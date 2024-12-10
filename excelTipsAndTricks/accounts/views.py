from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
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
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(UnauthenticatedOnlyMixin, FormView):
    template_name = 'accounts/register-page.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        user.email = form.cleaned_data['email']
        user.save()
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
        logout(request)
        return render(request, 'accounts/logout-page.html')

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')

        logout(request)
        return render(request, 'accounts/logout-page.html')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password-change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been successfully changed.')

        logout(self.request)

        return super().form_valid(form)


class ProfilePageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['user_profile'] = user_profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile-update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please fix the errors below.')
        return self.render_to_response(self.get_context_data(form=form))


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/profile-delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must be logged in to delete your account.')
            return redirect('login')
        return super().dispatch(*args, **kwargs)

    def get_object(self, queryset=None):

        return self.request.user

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):

        password = request.POST.get('password')

        user = request.user
        user_authenticated = authenticate(username=user.username, password=password)

        if user_authenticated is not None:
            self.get_object().delete()
            messages.success(request, 'Your account has been deleted.')
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('profile_delete')
