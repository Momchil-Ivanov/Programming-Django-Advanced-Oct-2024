from django.contrib import admin
from .models import Tip


class TipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # If the user is a staff member, they can see all tips
        if request.user.is_staff:
            return queryset

        # Otherwise, limit to the tips created by the user
        return queryset.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        # Allow staff users to change any tip
        if request.user.is_staff:
            return True
        # Otherwise, only allow changing their own tips
        if obj is not None and obj.author == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow staff users to delete any tip
        if request.user.is_staff:
            return True
        # Otherwise, only allow deleting their own tips
        if obj is not None and obj.author == request.user:
            return True
        return False


admin.site.register(Tip, TipAdmin)