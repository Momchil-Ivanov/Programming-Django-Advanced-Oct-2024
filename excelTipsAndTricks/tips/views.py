from channels.db import database_sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from .models import Tip
from .forms import TipForm
from ..categories.models import Category
from ..common.forms import CommentForm
from ..common.models import Comment, LikeDislike
from ..tags.models import Tag


class AllTipsView(LoginRequiredMixin, ListView):
    model = Tip
    template_name = 'tips/tip-list-page.html'
    context_object_name = 'tips'
    paginate_by = 5

    def get_queryset(self):
        return Tip.objects.all().order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']

        start_index = max(1, page_obj.number - 5)
        end_index = min(page_obj.paginator.num_pages + 1, page_obj.number + 6)

        context['custom_page_range'] = range(start_index, end_index)
        return context


class CreateTipView(LoginRequiredMixin, CreateView):
    model = Tip
    form_class = TipForm
    template_name = 'tips/tip-add-page.html'
    success_url = reverse_lazy('all_tips')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        return response

    def form_invalid(self, form):

        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")

        return self.render_to_response({'form': form})


class EditTipView(LoginRequiredMixin, UpdateView):
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
        form.instance.tags.set(form.cleaned_data['tags'])
        form.instance.categories.set(form.cleaned_data['categories'])

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        return self.render_to_response(self.get_context_data(form=form))

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user and not self.request.user.is_superuser and not self.request.user.is_staff:
            messages.error(self.request, "You do not have permission to edit this tip.")
            return redirect('all_tips')
        return super().dispatch(request, *args, **kwargs)


class TipDetailView(LoginRequiredMixin, DetailView):
    model = Tip
    template_name = 'tips/tip-details-page.html'
    context_object_name = 'tip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(tip=self.object).order_by('-created_at')
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['comments'] = page_obj
        context['comment_form'] = CommentForm()
        return context


class TipDeleteView(LoginRequiredMixin, DeleteView):
    model = Tip
    template_name = 'tips/tip-delete-page.html'
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user and not self.request.user.is_superuser and not self.request.user.is_staff:

            messages.error(self.request, "You do not have permission to delete this tip.")
            return None
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is None:
            return redirect('all_tips')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@database_sync_to_async
def like_tip_sync(request, pk):
    tip = get_object_or_404(Tip, pk=pk)

    LikeDislike.objects.filter(user=request.user, tip=tip, action=LikeDislike.DISLIKE).delete()

    existing_like = LikeDislike.objects.filter(user=request.user, tip=tip, action=LikeDislike.LIKE).exists()

    with transaction.atomic():
        if existing_like:
            LikeDislike.objects.filter(user=request.user, tip=tip, action=LikeDislike.LIKE).delete()
            messages.info(request, 'You removed your like.')
        else:
            LikeDislike.objects.create(user=request.user, tip=tip, action=LikeDislike.LIKE)
            messages.success(request, 'You liked this tip.')

    return redirect('tip_detail', pk=pk)


@login_required()
async def like_tip(request, pk):
    return await like_tip_sync(request, pk)


@database_sync_to_async
def dislike_tip_sync(request, pk):
    tip = get_object_or_404(Tip, pk=pk)

    LikeDislike.objects.filter(user=request.user, tip=tip, action=LikeDislike.LIKE).delete()

    existing_dislike = LikeDislike.objects.filter(user=request.user, tip=tip, action=LikeDislike.DISLIKE).exists()

    with transaction.atomic():
        if existing_dislike:
            LikeDislike.objects.filter(user=request.user, tip=tip, action=LikeDislike.DISLIKE).delete()
            messages.info(request, 'You removed your dislike.')
        else:
            LikeDislike.objects.create(user=request.user, tip=tip, action=LikeDislike.DISLIKE)
            messages.success(request, 'You disliked this tip.')

    return redirect('tip_detail', pk=pk)


@login_required
async def dislike_tip(request, pk):
    return await dislike_tip_sync(request, pk)


def login_required_with_message(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You need to be logged in to access comments.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


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
    return redirect('tip_detail', pk=tip.pk)


@login_required_with_message
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author and not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect('tip_detail', pk=comment.tip.pk)

    tip = comment.tip
    comment.delete()
    messages.success(request, 'The comment has been deleted.')
    return redirect('tip_detail', pk=tip.pk)


@login_required_with_message
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

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
    exclude_ids = [int(id) for id in exclude_ids if id.isdigit()]

    if search_query:
        categories = Category.objects.filter(name__icontains=search_query).exclude(id__in=exclude_ids)
    else:
        categories = Category.objects.exclude(id__in=exclude_ids)

    results = [{'id': category.id, 'name': category.name} for category in categories]
    return JsonResponse({'categories': results})


@login_required
def tag_search(request):
    search_query = request.GET.get('q', '').strip()
    exclude_ids = request.GET.get('exclude_ids', '').split(',')
    exclude_ids = [int(id) for id in exclude_ids if id.isdigit()]

    if search_query:
        tags = Tag.objects.filter(name__icontains=search_query).exclude(id__in=exclude_ids)
    else:
        tags = Tag.objects.exclude(id__in=exclude_ids)

    results = [{"id": tag.id, "name": tag.name} for tag in tags]
    return JsonResponse({"tags": results})
