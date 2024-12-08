from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from excelTipsAndTricks.common.models import AboutPage
from excelTipsAndTricks.common.serializers import AboutPageSerializer
import requests


# Class-based view for the Home page
class HomePageView(TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the user is logged in and if there's a success message to show
        if self.request.user.is_authenticated:
            # Show success message after successful login on home page
            if messages.get_messages(self.request):
                # Clear the success message if it's shown already
                messages.get_messages(self.request).used = True

        return context


# class AboutPageView(TemplateView):
#     template_name = 'common/about.html'

# REST API View for About page data
class AboutPageView(TemplateView):
    template_name = 'common/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data from the About Page API
        try:
            response = requests.get('http://127.0.0.1:8000/api/about/')
            if response.status_code == 200:
                about_data = response.json()
                context['title'] = about_data.get('title', 'Default Title')
                context['description'] = about_data.get('description', 'Default description.')
            else:
                context['title'] = 'About - Excel Tips and Tricks'
                context['description'] = 'We are passionate about helping you improve your Excel skills with the best tips and tricks!'
        except requests.exceptions.RequestException as e:
            # Handle error if the API is down or unreachable
            context['title'] = 'About - Excel Tips and Tricks'
            context['description'] = 'We are passionate about helping you improve your Excel skills with the best tips and tricks!'
            print(f"Error fetching About page data: {e}")

        return context


class AboutPageApiView(APIView):
    def get(self, request, *args, **kwargs):
        about_page = AboutPage.objects.first()  # Fetch first AboutPage object
        if not about_page:
            return Response({'error': 'AboutPage not found'}, status=404)

        serializer = AboutPageSerializer(about_page)
        return Response(serializer.data)