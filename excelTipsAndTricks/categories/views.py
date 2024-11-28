from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Category
from .forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category-list-page.html'
    context_object_name = 'categories'
    login_url = '/login/'  # Redirect unauthenticated users to login

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Category.objects.count() == 0:
            context['no_categories_message'] = "No Categories Created"
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-add-page.html'
    success_url = reverse_lazy('view_category')
    login_url = '/login/'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-edit-page.html'
    success_url = reverse_lazy('view_category')
    login_url = '/login/'


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category-delete-page.html'
    success_url = reverse_lazy('view_category')
    login_url = '/login/'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'categories/category-details-page.html'
    context_object_name = 'category'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tips'] = self.object.tips.all()
        return context
