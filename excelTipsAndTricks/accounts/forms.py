from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture_url', 'website', 'age', 'email']
        widgets = {
            'profile_picture_url': forms.URLInput(attrs={'placeholder': 'Enter URL for profile picture'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'website': forms.URLInput(attrs={'placeholder': 'Your website (optional)'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Your age'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email is being changed and if it's already in use
        if email:
            user = self.instance.user  # Get the current user
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise forms.ValidationError("This email address is already in use by another account.")
        return email

    def save(self, commit=True):
        # Save the profile data
        user_profile = super().save(commit=False)

        # Update the user's email
        if 'email' in self.cleaned_data:
            user_profile.user.email = self.cleaned_data['email']
            user_profile.user.save()

        # Save the profile
        if commit:
            user_profile.save()
        return user_profile

    def clean(self):
        cleaned_data = super().clean()
        profile_picture = cleaned_data.get('profile_picture')  # This assumes `profile_picture` exists in the model
        profile_picture_url = cleaned_data.get('profile_picture_url')

        # Ensure only one of profile_picture or profile_picture_url is filled
        if profile_picture and profile_picture_url:
            raise forms.ValidationError(
                "Please provide only one profile picture: either upload an image or provide an external URL."
            )
        return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))