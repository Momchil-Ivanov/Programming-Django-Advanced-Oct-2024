import os

import requests
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
from excelTipsAndTricks.common.serializers import WeatherSerializer
from django.core.cache import cache


def get_client_ip(request):
    # Get the X-Forwarded-For header which contains the real IP address of the client
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # The first IP in the X-Forwarded-For list is the real client IP
    else:
        ip = request.META.get('REMOTE_ADDR')  # Fallback to REMOTE_ADDR if X-Forwarded-For is not present

    # If running locally (localhost or 127.0.0.1), dynamically get the public IP
    if ip in ["127.0.0.1", "::1"]:  # Local development environment
        cached_ip = cache.get('client_ip')
        if not cached_ip:
            try:
                # Get the public IP address using an external service like ipify
                response = requests.get("https://api.ipify.org?format=json")
                if response.status_code == 200:
                    ip = response.json().get("ip", "8.8.8.8")  # Default to a known IP if fetching fails
                    # Cache the IP for 5 minutes
                    cache.set('client_ip', ip, timeout=300)
            except requests.RequestException:
                ip = "8.8.8.8"  # Fallback IP for testing in case the external service fails

    return ip


def get_user_location(request):
    ip = get_client_ip(request)
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        if response.status_code == 200:
            location_data = response.json()
            city = location_data.get('city', 'Berlin')
            return city
        else:
            return 'Berlin'
    except requests.exceptions.RequestException:
        return 'Berlin'


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
        else:
            return {'error': 'Unable to fetch weather data'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Error fetching weather data: {e}'}


class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        city = get_user_location(self.request)
        weather_data = fetch_weather_data(city)

        print(weather_data)

        context['weather'] = weather_data

        return context


class WeatherApiView(APIView):
    def get(self, request, *args, **kwargs):
        city = request.GET.get('city', 'Berlin')

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
