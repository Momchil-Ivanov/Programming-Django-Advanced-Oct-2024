from django.db import models


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

    def __str__(self):
        return self.name
