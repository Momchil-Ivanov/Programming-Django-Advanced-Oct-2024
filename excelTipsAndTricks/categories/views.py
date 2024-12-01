from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Category
from .forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category-list-page.html'
    context_object_name = 'categories'
    login_url = '/login/'  # Redirect unauthenticated users to login
    paginate_by = 5  # Number of categories per page

    def get_queryset(self):
        # Order categories alphabetically by name
        return Category.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = context['page_obj']

        # Show first and last five pages around the current page
        page_range = paginator.page_range
        current_page = page.number
        total_pages = paginator.num_pages

        range_start = max(1, current_page - 5)
        range_end = min(total_pages + 1, current_page + 5)

        context['custom_page_range'] = page_range[range_start - 1:range_end]

        if Category.objects.count() == 0:
            context['no_categories_message'] = "No Categories Created"

        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-add-page.html'
    success_url = reverse_lazy('view_category')
    login_url = '/login/'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add debug print to log errors
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        return self.render_to_response({'form': form})

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-edit-page.html'
    success_url = reverse_lazy('view_category')
    login_url = '/login/'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        # Add debug print to log errors
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        return self.render_to_response({'form': form})


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category-delete-page.html'
    context_object_name = 'object'
    login_url = '/login/'
    success_url = reverse_lazy('view_category')

    def get_object(self, queryset=None):
        # Ensure we are deleting the correct category
        return get_object_or_404(Category, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        # This should show the confirmation page before performing the delete
        category = self.get_object()
        return self.render_to_response({'object': category})

    def post(self, request, *args, **kwargs):
        # Perform the deletion after confirmation
        category = self.get_object()
        messages.success(self.request, f'Category "{category.name}" has been successfully deleted.')
        return super().post(request, *args, **kwargs)

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'categories/category-details-page.html'
    context_object_name = 'category'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tips'] = self.object.tips.all()
        return context
