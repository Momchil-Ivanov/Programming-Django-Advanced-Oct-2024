from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    email = models.EmailField(
        unique=True,
        blank=False,
    )

    bio = models.TextField(
        blank=True,
        null=True,
    )

    profile_picture_url = models.URLField(
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True,
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    is_approved = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_profile_picture(self):
        # Return the profile picture URL or a placeholder if not provided
        return self.profile_picture_url or '/static/images/accounts/default_profile_picture.jpg'
