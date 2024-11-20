# tags/urls.py
from django.urls import path
from .views import tag_autocomplete, TagSearchView

urlpatterns = [
    path('tag-autocomplete/', tag_autocomplete, name='tag_autocomplete'),  # Autocomplete for tags
    path('search/', TagSearchView.as_view(), name='search_tags'),  # View for tag search
]