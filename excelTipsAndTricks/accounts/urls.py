from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', TemplateView.as_view(template_name='accounts/password-change-done.html'), name='password_change_done'),
    path('profile/', views.ProfilePageView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
]
