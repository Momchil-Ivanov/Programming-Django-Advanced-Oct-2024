from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )

    search_fields = (
        'name',
    )

    def image_url(self, obj):
        return f'<img src="{obj.image_url}" style="width: 50px; height: 50px;" />'
    image_url.allow_tags = True
