from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.shortcuts import redirect, render
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

@user_passes_test(lambda u: u.is_staff or u.is_superuser)  # Ensure only staff or superusers can access
def manage_tags(request):
    query = request.GET.get('query', '')  # Get the search query from GET request (if any)
    if query:
        tags = Tag.objects.filter(Q(name__icontains=query))  # Case-insensitive search for tags
    else:
        tags = Tag.objects.all()  # If no query, show all tags

    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        try:
            tag = Tag.objects.get(id=tag_id)
            tag.delete()
            messages.success(request, "Tag deleted successfully.")
        except Tag.DoesNotExist:
            messages.error(request, "Tag not found.")
        return redirect('manage_tags')  # Redirect to the same page after deleting

    return render(request, 'tags/tag_manage.html', {'tags': tags, 'query': query})


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