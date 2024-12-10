from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        count, _ = queryset.delete()
        self.message_user(request, f"{count} tag(s) were deleted.")
    delete_selected.short_description = "Delete selected tags"
