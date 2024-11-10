from django.db import models
from django.contrib.auth.models import User
from excelTipsAndTricks.tips.models import Tip


class Comment(models.Model):
    tip = models.ForeignKey(
        Tip,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.tip.title}"


class LikeDislike(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'

    ACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='like_dislikes',
    )

    tip = models.ForeignKey(
        Tip,
        on_delete=models.CASCADE,
        related_name='like_dislikes',
    )

    action = models.CharField(
        max_length=7,
        choices=ACTION_CHOICES,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.user.username} {self.action}d {self.tip.title}"

    class Meta:
        unique_together = ('user', 'tip')  # Ensures one action per user per tip
