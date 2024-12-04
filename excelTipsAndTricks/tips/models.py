from django.db import models
from django.contrib.auth.models import User
from excelTipsAndTricks.categories.models import Category
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

    # Changed likes and dislikes to represent specific actions and improve consistency
    likes = models.ManyToManyField(
        User,
        related_name='liked_tips',
        blank=True,
    )

    dislikes = models.ManyToManyField(
        User,
        related_name='disliked_tips',
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='tips',
        blank=True,
    )

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()