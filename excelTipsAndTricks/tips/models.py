from django.db import models
from django.contrib.auth.models import User
from excelTipsAndTricks.categories.models import Category
from excelTipsAndTricks.common.models import LikeDislike
from excelTipsAndTricks.tags.models import Tag


class Tip(models.Model):
    title = models.CharField(
        unique=True,
        max_length=50,
    )

    content = models.TextField()

    image_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional URL for an image to display under the title.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tips',
    )

    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='tips',
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='tips',
        blank=True,
    )

    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.like_dislikes.filter(action=LikeDislike.LIKE).count()

    def total_dislikes(self):
        return self.like_dislikes.filter(action=LikeDislike.DISLIKE).count()
