from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
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
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-add-page.html'
    success_url = reverse_lazy('view_category')  # Redirect to the category list page after creation


# Edit an existing category
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-edit-page.html'
    success_url = reverse_lazy('view_category')  # Redirect to the category list page after editing


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/category-delete-page.html'
    success_url = reverse_lazy('view_category')  # Redirect to the category list page after deletion

    def post(self, request, *args, **kwargs):
        # Add any custom logic here if needed
        return super().post(request, *args, **kwargs)
