from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )

    search_fields = ('name',)

    def image_url(self, obj):
        return f'<img src="{obj.image_url}" style="width: 50px; height: 50px;" />'

    image_url.allow_tags = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # If the user is a staff member, they can see all categories
        if request.user.is_staff:
            return queryset

        return queryset  # You can add custom filtering logic if needed for non-staff users.

    def has_change_permission(self, request, obj=None):
        # Allow staff users to change any category
        if request.user.is_staff:
            return True
        # For normal users, deny edit permissions
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow staff users to delete any category
        if request.user.is_staff:
            return True
        # For normal users, deny delete permissions
        return False