import os
import requests
from django.http import JsonResponse
from django.shortcuts import render

from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config

from excelTipsAndTricks.common.forms import CityForm
from excelTipsAndTricks.common.serializers import WeatherSerializer


def fetch_weather_data(city):
    api_key = os.getenv('API_KEY', config('API_KEY'))
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_info = {
                'city': weather_data['name'],
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'icon': weather_data['weather'][0]['icon'],
            }
            return weather_info
        elif response.status_code == 404:
            return {'error': 'City not found'}
        else:
            return {'error': 'Unable to fetch weather data'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Error fetching weather data: {e}'}


def get_user_location(latitude=None, longitude=None):
    if latitude and longitude:
        geocode_url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={os.getenv("API_KEY", config("API_KEY"))}&units=metric'
        response = requests.get(geocode_url)
        if response.status_code == 200:
            location_data = response.json()
            return location_data['name']
    return 'Nowhere'


def update_location(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)

            city = get_user_location(latitude, longitude)

            weather_data = fetch_weather_data(city)

            if 'error' in weather_data:
                return JsonResponse({'error': weather_data['error']}, status=400)

            return JsonResponse({'message': 'Location updated', 'weather': weather_data})
        except ValueError:
            return JsonResponse({'error': 'Invalid latitude or longitude'}, status=400)
    else:
        return JsonResponse({'error': 'No location data provided'}, status=400)


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city_form = CityForm()

        city = kwargs.get('city', None)
        if not city:
            city = get_user_location()

        weather_data = fetch_weather_data(city)

        context['weather'] = weather_data
        context['city_form'] = city_form

        return context

    def post(self, request, *args, **kwargs):
        city_form = CityForm(request.POST)
        if city_form.is_valid():
            city = city_form.cleaned_data['city']

            if not city:
                return self.get(request, *args, **kwargs)

            weather_data = fetch_weather_data(city)

            return render(request, self.template_name, {
                'weather': weather_data,
                'city_form': city_form,
            })

        return render(request, self.template_name, {'city_form': city_form})


class WeatherApiView(APIView):
    def get(self, request, *args, **kwargs):
        city = request.GET.get('city', 'Nowhere')

        weather_info = fetch_weather_data(city)

        if 'error' in weather_info:
            return Response({'error': weather_info['error']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WeatherSerializer(weather_info)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AboutPageView(TemplateView):
    template_name = 'common/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'About - Excel Tips and Tricks'
        context['description'] = ('We are passionate about helping you improve your '
                                  'Excel skills with the best tips and tricks!')

        return context
