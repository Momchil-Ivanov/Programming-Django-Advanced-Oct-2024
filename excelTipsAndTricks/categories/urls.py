from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='view_category'),
    path('create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
