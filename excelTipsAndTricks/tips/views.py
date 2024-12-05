from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Tip
from .forms import TipForm
from ..categories.models import Category
from ..common.forms import CommentForm
from ..common.models import Comment
from ..tags.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class AllTipsView(LoginRequiredMixin, ListView):
    model = Tip
    template_name = 'tips/tip-list-page.html'
    context_object_name = 'tips'
    paginate_by = 5  # Show 5 tips per page

    login_url = '/login/'  # Redirect unauthenticated users to login

    def get_queryset(self):
        # Sort the tips alphabetically by title
        return Tip.objects.all().order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']

        # Adjust indices to show 5 pages before and after
        start_index = max(1, page_obj.number - 5)  # At least 5 pages before the current page
        end_index = min(page_obj.paginator.num_pages + 1, page_obj.number + 6)

        context['custom_page_range'] = range(start_index, end_index)
        return context


class CreateTipView(CreateView):
    model = Tip
    form_class = TipForm
    template_name = 'tips/tip-add-page.html'
    success_url = reverse_lazy('all_tips')


    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the current user as the author
        response = super().form_valid(form)  # Save the tip

        return response

    def form_invalid(self, form):

        # Display the error message to the user
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")

        # Return the response with the form
        return self.render_to_response({'form': form})


class EditTipView(UpdateView):
    model = Tip
    form_class = TipForm
    template_name = 'tips/tip-edit-page.html'
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category_ids'] = list(self.object.categories.values_list('id', flat=True))
        context['selected_tag_ids'] = list(self.object.tags.values_list('id', flat=True))
        return context

    def form_valid(self, form):
        # Handle tags: create new tags if they do not exist
        tags = form.cleaned_data.get('tags', [])
        existing_tags = Tag.objects.all()

        # Iterate through each tag and create it if it does not exist
        for tag in tags:
            if not existing_tags.filter(name=tag.name.lower()).exists():
                new_tag = Tag(name=tag.name.lower())
                new_tag.save()

        # Set tags and categories after validation
        form.instance.tags.set(form.cleaned_data['tags'])
        form.instance.categories.set(form.cleaned_data['categories'])

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        return self.render_to_response(self.get_context_data(form=form))


class TipDetailView(DetailView):
    model = Tip
    template_name = 'tips/tip-details-page.html'
    context_object_name = 'tip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginate comments (5 comments per page)
        comments = Comment.objects.filter(tip=self.object).order_by('-created_at')
        paginator = Paginator(comments, 5)  # Show 5 comments per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['comments'] = page_obj
        context['comment_form'] = CommentForm()  # Ensure you pass the comment form as well
        return context


class TipDeleteView(DeleteView):
    model = Tip
    template_name = 'tips/tip-delete-page.html'  # Confirmation page
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')  # Redirect after deletion

    def get_queryset(self):
        # Ensures only the tip's author can delete the tip
        if self.request.user.is_staff:
            return Tip.objects.all()
        else:
            return Tip.objects.filter(author=self.request.user)

    def get(self, request, *args, **kwargs):
        # Show confirmation page when GET request is made
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Handle deletion when the user confirms it
        return super().post(request, *args, **kwargs)


@login_required
def like_tip(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.user in tip.dislikes.all():
        tip.dislikes.remove(request.user)
    if request.user not in tip.likes.all():
        tip.likes.add(request.user)
        messages.success(request, 'You liked this tip.')
    else:
        tip.likes.remove(request.user)
        messages.info(request, 'You removed your like.')
    return redirect('tip_detail', pk=pk)


@login_required
def dislike_tip(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    if request.user in tip.likes.all():
        tip.likes.remove(request.user)
    if request.user not in tip.dislikes.all():
        tip.dislikes.add(request.user)
        messages.success(request, 'You disliked this tip.')
    else:
        tip.dislikes.remove(request.user)
        messages.info(request, 'You removed your dislike.')
    return redirect('tip_detail', pk=pk)


@login_required
@require_POST
def add_comment(request, pk):
    tip = get_object_or_404(Tip, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.tip = tip
        comment.author = request.user
        comment.save()
        messages.success(request, 'Your comment has been added.')
    else:
        messages.error(request, 'Failed to add comment. Please try again.')
    return redirect('tip_detail', pk=tip.pk)  # Redirecting to the tip page


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to delete this comment.")

    tip = comment.tip  # Keep track of the tip before deleting
    comment.delete()
    messages.success(request, 'The comment has been deleted.')
    return redirect('tip_detail', pk=tip.pk)  # Redirect to the tip page


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Ensure that the user is the author, superuser, or staff to edit the comment
    if request.user == comment.author or request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your comment has been updated.')
                return redirect('tip_detail', pk=comment.tip.pk)
        else:
            form = CommentForm(instance=comment)

        return render(request, 'tips/tip-comment-edit.html', {'form': form})
    else:
        messages.error(request, 'You are not authorized to edit this comment.')
        return redirect('tip_detail', pk=comment.tip.pk)


@login_required
def category_search(request):
    search_query = request.GET.get('q', '').strip()
    exclude_ids = request.GET.get('exclude_ids', '').split(',')
    exclude_ids = [int(id) for id in exclude_ids if id.isdigit()]  # Convert to list of integers

    if search_query:
        categories = Category.objects.filter(name__icontains=search_query).exclude(id__in=exclude_ids)
    else:
        categories = Category.objects.exclude(id__in=exclude_ids)

    # Return the filtered categories as JSON
    results = [{'id': category.id, 'name': category.name} for category in categories]
    return JsonResponse({'categories': results})

@login_required
def tag_search(request):
    search_query = request.GET.get('q', '').strip()
    exclude_ids = request.GET.get('exclude_ids', '').split(',')
    exclude_ids = [int(id) for id in exclude_ids if id.isdigit()]

    if search_query:
        # Filter tags based on the search query and exclude already selected ones
        tags = Tag.objects.filter(name__icontains=search_query).exclude(id__in=exclude_ids)
    else:
        # Exclude already selected tags even when no search query is entered
        tags = Tag.objects.exclude(id__in=exclude_ids)

    # Return the filtered tags as JSON
    results = [{"id": tag.id, "name": tag.name} for tag in tags]
    return JsonResponse({"tags": results})