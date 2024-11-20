from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Tip
from .forms import TipForm
from ..tags.models import Tag

class AllTipsView(ListView):
    model = Tip
    template_name = 'tips/tip-list-page.html'
    context_object_name = 'tips'

    def get_queryset(self):
        return Tip.objects.filter(author=self.request.user)

class CreateTipView(CreateView):
    model = Tip
    form_class = TipForm
    template_name = 'tips/tip-add-page.html'
    success_url = reverse_lazy('all_tips')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as the author
        response = super().form_valid(form)

        # Process tags from the input field
        tags_input = self.request.POST.get('tags')
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]  # Split by commas
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                tag_objects.append(tag_obj)
            form.instance.tags.set(tag_objects)  # Associate the tags with the tip instance
        else:
            form.instance.tags.clear()  # Clear tags if none provided

        return response

class EditTipView(UpdateView):
    model = Tip
    form_class = TipForm
    template_name = 'tips/tip-edit-page.html'
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')  # Redirect to the list of all tips after updating

    def get_queryset(self):
        return Tip.objects.filter(author=self.request.user)

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Process tags (from a custom input field)
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

    def get_object(self, queryset=None):
        # Ensure the tip is only accessible by the author or admin
        obj = super().get_object(queryset)
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to view this tip.")
        return obj

class TipDeleteView(DeleteView):
    model = Tip
    template_name = 'tips/tip-delete-page.html'
    context_object_name = 'tip'
    success_url = reverse_lazy('all_tips')  # Redirect to My Tips after deletion

    def get_queryset(self):
        # Ensure the tip is only deletable by the author or admin
        return Tip.objects.filter(author=self.request.user)

    def form_valid(self, form):
        # You can perform additional checks before deletion if needed
        return super().form_valid(form)