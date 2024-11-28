from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Category
from .forms import CategoryForm


# View all categories
class CategoryListView(ListView):
    model = Category
    template_name = 'categories/category-list-page.html'  # Updated template name
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if there are no categories and pass a custom message
        if Category.objects.count() == 0:
            context['no_categories_message'] = "No Categories Created"
        return context


# Create new category
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-add-page.html'
    success_url = reverse_lazy('view_category')  # Redirect to the category list page after creation

    # Customize the redirect URL for non-logged-in users
    login_url = '/login/'  # Redirect to login if not logged in

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-edit-page.html'
    success_url = reverse_lazy('view_category')  # Redirect to the category list page after editing

    login_url = '/login/'  # Redirect to login if not logged in

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category-delete-page.html'
    success_url = reverse_lazy('view_category')  # Redirect to the category list page after deletion

    login_url = '/login/'  # Redirect to login if not logged in

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/category-details-page.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tips'] = self.object.tips.all()  # Corrected to use the related_name
        return context
