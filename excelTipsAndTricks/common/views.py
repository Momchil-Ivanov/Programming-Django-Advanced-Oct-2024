from django.shortcuts import render
from django.views.generic import TemplateView


# Class-based view for the Home page
class HomePageView(TemplateView):
    template_name = 'common/home.html'


class AboutPageView(TemplateView):
    template_name = 'common/about.html'
