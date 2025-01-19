from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_tags')
    search_fields = ('name', 'description', 'tags__name')
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

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
