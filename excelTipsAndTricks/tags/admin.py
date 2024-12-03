from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    # You can enable or disable actions as needed. Deletion is enabled by default.
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        # Custom action for bulk deletion (optional)
        count, _ = queryset.delete()
        self.message_user(request, f"{count} tag(s) were deleted.")
    delete_selected.short_description = "Delete selected tags"
