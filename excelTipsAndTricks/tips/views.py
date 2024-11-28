from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Tip
from .forms import TipForm
from ..common.forms import CommentForm
from ..tags.models import Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class AllTipsView(ListView):
    model = Tip
    template_name = 'tips/tip-list-page.html'
    context_object_name = 'tips'

    def get_queryset(self):
        # Fetch all tips for public viewing (no filtering)
        return Tip.objects.all()


class CreateTipView(CreateView):
    model = Tip
    form_class = TipForm
    template_name = 'tips/tip-add-page.html'
    success_url = reverse_lazy('all_tips')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Process tags
        tags_input = self.request.POST.get('tags')
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                tag_objects.append(tag_obj)
            form.instance.tags.set(tag_objects)

        return response


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
            tags = [tag.strip() for tag in tags_input.split(',')]
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                tag_objects.append(tag_obj)
            form.instance.tags.set(tag_objects)

        return response


class TipDetailView(DetailView):
    model = Tip
    template_name = 'tips/tip-view-page.html'
    context_object_name = 'tip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tip = self.get_object()
        context['comments'] = tip.comments.order_by('-created_at')  # Fetch comments for this tip
        context['comment_form'] = CommentForm()  # Add the comment form to the context
        return context


class TipDeleteView(DeleteView):
    model = Tip
    template_name = 'tips/tip-delete-page.html'
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')  # Redirect to All Tips after deletion

    def get_queryset(self):
        # Ensure only the author or superuser can delete the tip
        return Tip.objects.filter(author=self.request.user)

    def form_valid(self, form):
        # You can perform additional checks before deletion if needed
        return super().form_valid(form)


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
    return redirect('tip_detail', pk=pk)