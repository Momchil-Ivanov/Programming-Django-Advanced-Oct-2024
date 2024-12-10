from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile
from .. import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        assign_role_to_user(instance, 'Regular')
        send_mail(
            subject="Welcome to Excel Tips and Tricks",
            message="We are excited to have you join our community! Here are some tips and tricks to help you improve your Excel skills.",
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def assign_role_to_user(user, role):
    try:
        group = Group.objects.get(name=role)
        user.groups.add(group)
    except Group.DoesNotExist:
        pass
