from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Customize the default UserAdmin
class CustomUserAdmin(UserAdmin):
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

# Register the custom UserAdmin (no need to re-register the User model)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Register UserProfile model separately
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'website', 'age', 'profile_picture_url')
    search_fields = ('user__username', 'bio', 'website')
    ordering = ('user__username',)  # Order by username
    list_filter = ('is_approved', 'age')