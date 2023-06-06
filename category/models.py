from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Category(models.Model):
    label = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.label


class CategorizedItem(models.Model):
    """What tag applied to what object
    with a generic reusable relationship"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Type (product, video, article, etc.)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
