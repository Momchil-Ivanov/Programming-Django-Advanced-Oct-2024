from django.urls import path
from . import views

urlpatterns = [
    path('all-tips/', views.AllTipsView.as_view(), name='all_tips'),
    path('create-tip/', views.CreateTipView.as_view(), name='create_tip'),
    path('edit-tip/<int:pk>/', views.EditTipView.as_view(), name='edit_tip'),
    path('details-tip/<int:pk>/', views.TipDetailView.as_view(), name='tip_detail'),
    path('delete-tip/<int:pk>/', views.TipDeleteView.as_view(), name='delete_tip'),
    path('like-tip/<int:pk>/', views.like_tip, name='like_tip'),
    path('dislike-tip/<int:pk>/', views.dislike_tip, name='dislike_tip'),
    path('<int:pk>/add-comment/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:pk>/', views.edit_comment, name='edit_comment'),  # Edit comment URL
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),  # Delete comment URL
    path('category-search/', views.category_search, name='category_search'),
    path('tag-search/', views.tag_search, name='tag_search'),
]
