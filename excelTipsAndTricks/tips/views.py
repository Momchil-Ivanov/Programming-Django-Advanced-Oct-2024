from django.contrib.auth.mixins import LoginRequiredMixin
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
        response = super().form_valid(form)  # Call the parent form_valid method to save the tip

        # Process tags
        tags_input = self.request.POST.get('tags')
        if tags_input:
            # Split the tags by commas, strip them, and create Tag objects
            tags = [tag.strip() for tag in tags_input.split(',')]
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                tag_objects.append(tag_obj)
            form.instance.tags.set(tag_objects)  # Use the set() method to assign the tags

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

    def get_queryset(self):
        # Only allow authors to edit their own tips
        return Tip.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Process tags
        tags_input = self.request.POST.get('tags')
        if tags_input:
            # Split the tags by commas, strip them, and create Tag objects
            tags = [tag.strip() for tag in tags_input.split(',')]
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                tag_objects.append(tag_obj)
            form.instance.tags.set(tag_objects)  # Use the set() method to assign the tags

        return response

    def form_invalid(self, form):
        # Add custom error message when the form is invalid
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        # Ensure that the form's current data, including the incorrect title, is passed back
        return self.render_to_response(self.get_context_data(form=form))

# class TipDetailView(DetailView):
#     model = Tip
#     template_name = 'tips/tip-view-page.html'
#     context_object_name = 'tip'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         tip = self.get_object()
#         context['comments'] = tip.comments.order_by('-created_at')  # Fetch comments for this tip
#         context['comment_form'] = CommentForm()  # Add the comment form to the context
#         return context

class TipDetailView(DetailView):
    model = Tip
    template_name = 'tips/tip-view-page.html'
    context_object_name = 'tip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tip = self.get_object()

        # Fetch associated comments for this tip, ordered by the most recent
        context['comments'] = tip.comments.order_by('-created_at')

        # Include the comment form
        context['comment_form'] = CommentForm()

        # Pass the tags related to this tip
        context['tags'] = tip.tags.all()

        return context


class TipDeleteView(DeleteView):
    model = Tip
    template_name = 'tips/tip-delete-page.html'  # Confirmation page
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')  # Redirect after deletion

    def get_queryset(self):
        # Ensures only the tip's author can delete the tip
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

def category_search(request):
    search_query = request.GET.get('q', '')
    exclude_ids = request.GET.get('exclude_ids', '')

    # Split the exclude_ids into a list, but only if it's not empty
    exclude_ids = [int(id) for id in exclude_ids.split(',') if id]

    # Filter categories based on search query and exclude selected categories
    categories = Category.objects.filter(name__icontains=search_query).exclude(id__in=exclude_ids)

    # Return the results as JSON
    results = [{'id': category.id, 'name': category.name} for category in categories]

    return JsonResponse({'categories': results})

# def tag_search(request):
#     search_query = request.GET.get('q', '')
#
#     # Get tags that match the search query
#     tags = Tag.objects.filter(name__icontains=search_query)
#
#     # Return the results as JSON
#     results = [{'id': tag.id, 'name': tag.name} for tag in tags]
#
#     return JsonResponse({'tags': results})

def tag_search(request):
    search_query = request.GET.get('q', '')
    exclude_ids = request.GET.get('exclude_ids', '').split(',')
    exclude_ids = [int(id) for id in exclude_ids if id]

    # Query for tags that match the search query, excluding selected ones
    tags = Tag.objects.filter(name__icontains=search_query).exclude(id__in=exclude_ids)

    # Ensure the response includes both existing and new tags
    results = [{"id": tag.id, "name": tag.name} for tag in tags]

    return JsonResponse({"tags": results})