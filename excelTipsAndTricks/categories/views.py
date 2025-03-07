from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Category
from .forms import CategoryForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category-list-page.html'
    context_object_name = 'categories'
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = context['page_obj']

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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        return self.render_to_response({'form': form})


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category-edit-page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        context['selected_tag_ids'] = [tag.id for tag in self.get_object().tags.all()]
        return context

    def get_success_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your form submission. Please fix the issues.")
        return self.render_to_response({'form': form})

    def dispatch(self, request, *args, **kwargs):
        category = self.get_object()
        if category.author != request.user and not request.user.is_staff and not request.user.is_superuser:
            messages.error(self.request, "You do not have permission to edit this category.")
            return redirect('view_category')
        return super().dispatch(request, *args, **kwargs)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category-delete-page.html'
    context_object_name = 'object'
    success_url = reverse_lazy('view_category')

    def get_object(self, queryset=None):
        return get_object_or_404(Category, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(self.request, f'Category "{category.name}" has been successfully deleted.')
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        category = self.get_object()
        if category.author != request.user and not request.user.is_staff and not request.user.is_superuser:
            messages.error(self.request, "You do not have permission to delete this category.")
            return redirect('view_category')
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'categories/category-details-page.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tips'] = self.object.tips.all()
        return context
