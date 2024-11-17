from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        assign_role_to_user(instance, 'Regular')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def assign_role_to_user(user, role):
    try:
        group = Group.objects.get(name=role)
        user.groups.add(group)
    except Group.DoesNotExist:
        pass