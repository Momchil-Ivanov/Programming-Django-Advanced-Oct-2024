from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomPasswordChangeForm, CustomAuthenticationForm  # Import CustomAuthenticationForm


# Registration View
class RegisterView(FormView):
    template_name = 'accounts/register-page.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Automatically log the user in after registration
        messages.success(self.request, "Registration successful. You are now logged in.")
        return super().form_valid(form)


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    form_class = CustomAuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, "Account or Password are not correct")
        return super().form_invalid(form)

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')  # Handle "remember me" checkbox
        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(2592000)  # 30 days
        return super().form_valid(form)


# Profile Page View
class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile
        context['user_profile'] = user_profile

        # Get the user's group/roles
        user_groups = self.request.user.groups.all()
        context['user_groups'] = user_groups

        return context


# Profile Update View
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile-update.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Fetching the profile of the logged-in user
        return self.request.user.profile

    def get_form_kwargs(self):
        # Pass the current user's email to the form as initial data
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'email': self.request.user.email}
        return kwargs


# Password Change View
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')


# Profile Delete View
class ProfileDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-delete.html'

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # If authentication is successful, delete the user and their profile
            request.user.delete()
            messages.success(request, 'Your profile has been deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('profile-delete')
