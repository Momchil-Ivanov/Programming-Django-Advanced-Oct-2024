from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

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
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'profile_picture_url', 'website', 'age']
        widgets = {
            'profile_picture_url': forms.URLInput(attrs={'placeholder': 'Enter URL for profile picture'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'website': forms.URLInput(attrs={'placeholder': 'Your website (optional)'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Your age'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            user = self.instance.user
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise forms.ValidationError("This email address is already in use by another account.")
        return email

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if 'email' in self.cleaned_data:
            user_profile.user.email = self.cleaned_data['email']
            user_profile.user.save()
        if commit:
            user_profile.save()
        return user_profile

    def clean(self):
        cleaned_data = super().clean()
        profile_picture = cleaned_data.get('profile_picture')
        profile_picture_url = cleaned_data.get('profile_picture_url')

        if profile_picture and profile_picture_url:
            raise forms.ValidationError(
                "Please provide only one profile picture: either upload an image or provide an external URL."
            )

        if not profile_picture and not profile_picture_url:
            raise forms.ValidationError(
                "Please provide at least one profile picture: either upload an image or provide an external URL."
            )

        return cleaned_data


class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New password',
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm new password',
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')

        # Check if new password is the same as the old password
        if new_password1 == old_password:
            raise forms.ValidationError("The new password cannot be the same as the old password.")
        return new_password1

    def clean_new_password2(self):
        new_password2 = self.cleaned_data.get('new_password2')
        new_password1 = self.cleaned_data.get('new_password1')

        # Check if both new passwords match
        if new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        return new_password2