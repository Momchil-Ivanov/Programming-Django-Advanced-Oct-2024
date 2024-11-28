from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView


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


class AboutPageView(TemplateView):
    template_name = 'common/about.html'
