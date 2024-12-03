from django.urls import path
from . import views  # Importing views module

urlpatterns = [
    path('tag-autocomplete/', views.tag_autocomplete, name='tag_autocomplete'),  # Autocomplete for tags
    path('search/', views.TagSearchView.as_view(), name='search_tags'),  # View for tag search
    path('manage-tags/', views.manage_tags, name='manage_tags'),  # Manage tags (view function)
    path('create-tag/', views.create_tags, name='create_tags'),  # Create a new tag
]