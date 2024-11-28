from django.db import models
from excelTipsAndTricks.tags.models import Tag  # Import Tag model


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    image_url = models.URLField(
        help_text="URL of the category image, mandatory field.",
    )
    tags = models.ManyToManyField(Tag, related_name='categories')  # Link categories to tags

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
