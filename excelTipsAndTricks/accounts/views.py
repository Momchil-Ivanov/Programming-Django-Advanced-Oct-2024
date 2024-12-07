from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages

from excelTipsAndTricks.accounts.forms import CustomPasswordChangeForm, ProfileUpdateForm, CustomUserCreationForm
from excelTipsAndTricks.accounts.models import UserProfile

class UnauthenticatedOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect to home if logged in
        return super().dispatch(request, *args, **kwargs)

class RegisterView(UnauthenticatedOnlyMixin, FormView):
    template_name = 'accounts/register-page.html'
    form_class = CustomUserCreationForm  # Your custom form
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the User first
        user = form.save()

        # Check if the UserProfile already exists
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # If the profile doesn't exist, create it
        if created:
            # Set any additional profile fields here if needed
            pass
        else:
            # Optionally, handle the case where the profile already exists
            pass

        # Update the email field on the User
        user.email = form.cleaned_data['email']
        user.save()

        # Add success message
        messages.success(self.request, 'Your account has been created. Please log in.')

        return super().form_valid(form)


class CustomLoginView(UnauthenticatedOnlyMixin, FormView):
    template_name = 'accounts/login-page.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'You are now logged in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


class CustomLogoutView(View):
    def post(self, request):
        # Log out the user and render the logout page with countdown
        logout(request)
        return render(request, 'accounts/logout-page.html')  # Show the countdown page

    def get(self, request):
        # Redirect unauthenticated users to the home page
        if not request.user.is_authenticated:
            return redirect('home')  # Redirect to home if the user is not logged in

        # If logged in, log out and show the logout page
        logout(request)
        return render(request, 'accounts/logout-page.html')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        # Change the password
        messages.success(self.request, 'Your password has been successfully changed.')

        # Log out the user after password change
        logout(self.request)

        # Redirect to the password change done page
        return super().form_valid(form)


class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)  # Ensure latest profile data
        context['user_profile'] = user_profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm  # Use the custom form here
    template_name = 'accounts/profile-update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Ensure we are getting the profile for the logged-in user
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        # Ensure the user profile is saved properly
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle form errors
        messages.error(self.request, 'Please fix the errors below.')
        return self.render_to_response(self.get_context_data(form=form))


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/profile-delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # Ensure the user is logged in before allowing access
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must be logged in to delete your account.')
            return redirect('login')  # Redirect to login if not logged in
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        # Ensure that we are deleting the current authenticated user
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Render the delete confirmation form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Handle password confirmation before deleting the user
        password = request.POST.get('password')

        # Authenticate the user with the entered password
        user = request.user
        user_authenticated = authenticate(username=user.username, password=password)

        if user_authenticated is not None:
            # If password is correct, delete the user and log them out
            self.get_object().delete()  # Delete the user object
            messages.success(request, 'Your account has been deleted.')
            logout(request)  # Log out the user
            return redirect('login')  # Redirect to login after deletion
        else:
            # If password is incorrect, show an error message
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('profile_delete')  # Redirect back to the delete page