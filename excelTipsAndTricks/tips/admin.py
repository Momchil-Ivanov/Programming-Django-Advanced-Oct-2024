from django.contrib import admin
from .models import Tip


class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_staff:
            return queryset

        return queryset.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        if obj is not None and obj.author == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_staff:
            return True
        if obj is not None and obj.author == request.user:
            return True
        return False


admin.site.register(Tip, TipAdmin)
