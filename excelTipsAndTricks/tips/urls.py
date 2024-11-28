from django.urls import path
from . import views
from .views import add_comment

urlpatterns = [
    path('all-tips/', views.AllTipsView.as_view(), name='all_tips'),
    path('create-tip/', views.CreateTipView.as_view(), name='create_tip'),
    path('edit-tip/<int:pk>/', views.EditTipView.as_view(), name='edit_tip'),
    path('details-tip/<int:pk>/', views.TipDetailView.as_view(), name='tip_detail'),
    path('delete-tip/<int:pk>/', views.TipDeleteView.as_view(), name='delete_tip'),
    path('like-tip/<int:pk>/', views.like_tip, name='like_tip'),
    path('dislike-tip/<int:pk>/', views.dislike_tip, name='dislike_tip'),
    path('<int:pk>/add-comment/', add_comment, name='add_comment'),
]