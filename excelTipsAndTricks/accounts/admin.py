from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserAdmin(UserAdmin):
    # Define the fields for user creation
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'user_permissions')
        }),
    )

    # Define the fields for editing an existing user
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'user_permissions')
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    actions = ['make_staff', 'make_superuser']

    def make_staff(self, request, queryset):
        queryset.update(is_staff=True)
        self.message_user(request, "Selected users have been made staff.")
    make_staff.short_description = "Make selected users staff"

    def make_superuser(self, request, queryset):
        queryset.update(is_staff=True, is_superuser=True)
        self.message_user(request, "Selected users have been made superusers.")
    make_superuser.short_description = "Make selected users superusers"


# Register the custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'website', 'age', 'profile_picture_url')
    search_fields = ('user__username', 'bio', 'website')
    ordering = ('user__username',)
    list_filter = ('is_approved', 'age')
