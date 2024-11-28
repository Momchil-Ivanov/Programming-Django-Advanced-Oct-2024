from django.contrib import admin
from .models import Category  # Import Category model

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)  # You can still search by category name and description

    # Exclude the 'tags' field completely from the admin form
    exclude = ('tags',)

    def image_url(self, obj):
        return f'<img src="{obj.image_url}" style="width: 50px; height: 50px;" />'

    image_url.allow_tags = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            return queryset
        return queryset

    def has_change_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        return False
