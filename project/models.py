from typing import Iterable, Optional
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Project(models.Model):
    featured_image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    github = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save function
        Set `self.slug` from `self.title` if none."""

        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
