from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('api/about/', views.AboutPageApiView.as_view(), name='about-api'),  # REST API endpoint
]
