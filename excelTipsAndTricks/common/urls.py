from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('api/weather/', views.WeatherApiView.as_view(), name='weather-api'),
    path('update-location/', views.update_location, name='update_location'),
]
