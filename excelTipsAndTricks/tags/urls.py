from django.urls import path
from . import views

urlpatterns = [
    path('tag-autocomplete/', views.tag_autocomplete, name='tag_autocomplete'),
    path('search/', views.TagSearchView.as_view(), name='search_tags'),
    path('manage-tags/', views.manage_tags, name='manage_tags'),
    path('create-tag/', views.create_tags, name='create_tags'),
    path('delete-tag/<int:tag_id>/', views.delete_tag, name='delete_tag'),
]
