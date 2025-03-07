from django.contrib.auth.models import User
from django.db import models
from excelTipsAndTricks.tags.models import Tag


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    image_url = models.URLField(
        help_text="URL of the category image, mandatory field.",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='categories'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
