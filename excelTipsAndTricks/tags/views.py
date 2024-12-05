from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView

from .forms import TagForm
from .models import Tag
from excelTipsAndTricks.tips.models import Tip
from excelTipsAndTricks.categories.models import Category

class TagSearchView(TemplateView):
    template_name = 'tags/tag_search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')  # Get the query parameter 'query'

        tags = Tag.objects.filter(name__icontains=query).distinct()
        tips = Tip.objects.filter(
            Q(title__icontains=query) |  # Use 'title' instead of 'name'
            Q(tags__name__icontains=query)  # Search for tags associated with tips
        ).distinct()
        categories = Category.objects.filter(
            Q(name__icontains=query) |  # Search for categories by name
            Q(tags__name__icontains=query)  # Assuming Category has a ManyToManyField to Tag
        ).distinct()

        # Pagination logic for tags, tips, and categories
        paginator_tags = Paginator(tags, 10)  # 10 items per page
        paginator_tips = Paginator(tips, 10)  # 10 items per page
        paginator_categories = Paginator(categories, 10)  # 10 items per page

        page_tags = self.request.GET.get('page_tags')  # Get the page number for tags
        page_tips = self.request.GET.get('page_tips')  # Get the page number for tips
        page_categories = self.request.GET.get('page_categories')  # Get the page number for categories

        # Get the corresponding page for each query
        tags_page_obj = paginator_tags.get_page(page_tags)
        tips_page_obj = paginator_tips.get_page(page_tips)
        categories_page_obj = paginator_categories.get_page(page_categories)

        # Calculate the page range (limit to 5 pages ahead or back)
        def get_page_range(page_obj):
            page_range = list(page_obj.paginator.page_range)

            # Calculate the start and end of the range to show
            start = max(page_obj.number - 5, 1)
            end = min(page_obj.number + 5, page_obj.paginator.num_pages)

            # Adjust the range to include 5 pages total
            if start > 1:
                page_range = page_range[start-1:end]
            elif end < page_obj.paginator.num_pages:
                page_range = page_range[start-1:end]

            return page_range

        context['tags'] = tags_page_obj
        context['tips'] = tips_page_obj
        context['categories'] = categories_page_obj
        context['query'] = query  # Include the search query for display

        # Add the page ranges for tags, tips, and categories
        context['tags_page_range'] = get_page_range(tags_page_obj)
        context['tips_page_range'] = get_page_range(tips_page_obj)
        context['categories_page_range'] = get_page_range(categories_page_obj)

        return context

@user_passes_test(lambda u: u.is_staff or u.is_superuser)  # Ensure only staff or superusers can access
def manage_tags(request):
    query = request.GET.get('query', '')
    if query:
        tags = Tag.objects.filter(name__icontains=query)
    else:
        tags = Tag.objects.all()

    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        try:
            tag = Tag.objects.get(id=tag_id)
            tag.delete()
            messages.success(request, "Tag deleted successfully.")
        except Tag.DoesNotExist:
            messages.error(request, "Tag not found.")
        return redirect('manage_tags')

    return render(request, 'tags/tag_manage.html', {'tags': tags, 'query': query})

@user_passes_test(lambda u: u.is_staff or u.is_superuser)  # Ensure only staff or superusers can access
def delete_tag(request, tag_id):
    # Get the tag to be deleted
    tag = get_object_or_404(Tag, id=tag_id)

    if request.method == 'POST':
        # Delete the tag if the form is submitted
        tag.delete()
        messages.success(request, "Tag deleted successfully.")
        return redirect('manage_tags')

    return render(request, 'tags/tag_delete.html', {'tag': tag})


def create_tags(request):
    if not request.user.is_authenticated or request.user.is_anonymous:
        return HttpResponseForbidden("You are not authorized to create tags.")

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            # Check if the tag already exists by name
            tag_name = form.cleaned_data['name'].lower()
            if Tag.objects.filter(name=tag_name).exists():
                print("Tag already exists.")  # Debugging line
                messages.error(request, "Tag already exists.")
            else:
                # Handle the creation of a new tag
                form.save()
                messages.success(request, "Tag created successfully!")
            return redirect('create_tags')  # Correct redirect to the 'create_tags' URL name
        else:
            # Print form errors to console for debugging
            print(form.errors)  # Debugging line
            messages.error(request, "There was an error with your form submission. Please try again.")

    else:
        form = TagForm()

    return render(request, 'tags/tag_create.html', {'form': form})

def tag_autocomplete(request):
    query = request.GET.get('q', '').strip()
    if query:
        tags = Tag.objects.filter(name__icontains=query)[:10]
        existing_tags = Tag.objects.all()[:5]  # Get a few existing tags for display
    else:
        tags = []
        existing_tags = Tag.objects.all()[:5]

    response_data = {
        'tags': [{'id': tag.id, 'text': tag.name} for tag in tags],
        'existing_tags': [{'id': tag.id, 'text': tag.name} for tag in existing_tags]
    }
    return JsonResponse(response_data)