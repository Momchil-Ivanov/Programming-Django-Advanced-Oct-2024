from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='view_category'),  # List categories
    path('create/', views.CategoryCreateView.as_view(), name='category_create'),  # Create category
    path('edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),  # Edit category
    path('delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),  # Delete category
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),  # Category details
]