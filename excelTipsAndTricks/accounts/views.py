from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


class RegisterView(FormView):
    template_name = 'accounts/register-page.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        form.save()  # Save the user to the database
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'

    def form_invalid(self, form):
        # Adding custom message to the message framework
        messages.error(self.request, "Account or Password are not correct")
        return super().form_invalid(form)
