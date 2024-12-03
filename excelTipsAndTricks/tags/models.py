from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def save(self, *args, **kwargs):
        # Ensure the tag name is always saved in lowercase
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name