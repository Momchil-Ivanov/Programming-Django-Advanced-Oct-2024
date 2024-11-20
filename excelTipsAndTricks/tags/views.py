from django.http import JsonResponse
from django.views.generic import ListView
from .models import Tag
from excelTipsAndTricks.tips.models import Tip  # Assuming the Tip model is in the 'tips' app

# Autocomplete view for tags
def tag_autocomplete(request):
    term = request.GET.get('term', '')  # Get the 'term' parameter from the GET request
    if term:  # Only perform the query if 'term' is provided
        tags = Tag.objects.filter(name__icontains=term).values('name')  # Case-insensitive search
        return JsonResponse(list(tags), safe=False)  # Return tags as a JSON response
    return JsonResponse([], safe=False)  # Return an empty list if no 'term' is provided

# Search view for tags (filtering tips by tags)
class TagSearchView(ListView):
    model = Tip  # You want to filter tips by tags, not just tags
    template_name = 'tags/tag_search_results.html'
    context_object_name = 'tips'  # We are displaying tips, not tags

    def get_queryset(self):
        query = self.request.GET.get('query', '')  # Get the query parameter 'query'
        if query:
            # Filter tips based on the tags' names matching the query (case-insensitive)
            return Tip.objects.filter(tags__name__icontains=query).distinct()
        return Tip.objects.none()  # Return no tips if no query is provided