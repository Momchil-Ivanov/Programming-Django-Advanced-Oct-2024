from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView
from .models import Tag
from excelTipsAndTricks.tips.models import Tip
from excelTipsAndTricks.categories.models import Category

# Autocomplete view for tags
def tag_autocomplete(request):
    term = request.GET.get('term', '')  # Get the 'term' parameter from the GET request
    exclude_ids = request.GET.get('exclude_ids', '')  # Get the exclude_ids parameter (comma-separated)

    # Convert exclude_ids into a list of tag names (or IDs) if provided
    exclude_ids = exclude_ids.split(',') if exclude_ids else []

    if term:  # Only perform the query if 'term' is provided
        # Filter tags by name, excluding any tags already selected
        tags = Tag.objects.filter(
            Q(name__icontains=term) & ~Q(name__in=exclude_ids)  # Case-insensitive search and exclude selected tags
        ).values('name')  # Return only the name field for the tags

        return JsonResponse(list(tags), safe=False)  # Return tags as a JSON response

    return JsonResponse([], safe=False)  # Return an empty list if no 'term' is provided

# Search view for tips and categories based on tags
class TagSearchView(TemplateView):
    template_name = 'tags/tag_search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')  # Get the query parameter 'query'

        # Search for tips by title or associated tags
        tips = Tip.objects.filter(
            Q(title__icontains=query) |  # Use 'title' instead of 'name'
            Q(tags__name__icontains=query)  # Search for tags associated with tips
        ).distinct()

        # Search for categories by name or associated tags
        categories = Category.objects.filter(
            Q(name__icontains=query) |  # Search for categories by name
            Q(tags__name__icontains=query)  # Assuming Category has a ManyToManyField to Tag
        ).distinct()

        # Pass tips and categories to the context
        context['tips'] = tips
        context['categories'] = categories
        context['query'] = query  # Include the search query for display
        return context
