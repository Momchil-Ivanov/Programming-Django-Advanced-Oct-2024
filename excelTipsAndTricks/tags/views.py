from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView
from .models import Tag
from excelTipsAndTricks.tips.models import Tip
from excelTipsAndTricks.categories.models import Category

# Autocomplete view for tags
def tag_autocomplete(request):
    term = request.GET.get('q', '')  # Select2 uses 'q' by default
    exclude_ids = request.GET.get('exclude_ids', '')

    # Parse exclude IDs if provided
    exclude_ids = [int(id) for id in exclude_ids.split(',') if id.isdigit()]

    if term:
        # Search for tags excluding provided IDs
        tags = Tag.objects.filter(
            Q(name__icontains=term) & ~Q(id__in=exclude_ids)
        ).values('id', 'name')  # Include IDs for Select2

        # Format data for Select2
        return JsonResponse({
            'tags': [{'id': tag['id'], 'text': tag['name']} for tag in tags]
        })

    return JsonResponse({'tags': []})

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
