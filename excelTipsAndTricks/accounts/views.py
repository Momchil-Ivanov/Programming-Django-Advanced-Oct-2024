from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
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
    redirect_authenticated_user = True  # Redirect logged-in users away from the login page
    next_page = reverse_lazy('home')  # Redirect to the home page after login
