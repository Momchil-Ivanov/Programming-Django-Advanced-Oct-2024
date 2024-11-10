from django.contrib import admin
from .models import Comment, LikeDislike


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'tip',
        'author',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'author__username',
        'tip__title',
        'content',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )


@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'tip',
        'action',
        'created_at',
    )

    search_fields = (
        'user__username',
        'tip__title',
    )

    list_filter = (
        'action',
        'created_at',
    )
