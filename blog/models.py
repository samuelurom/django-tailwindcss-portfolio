from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django_quill.fields import QuillField


class Tag(models.Model):
    """Model for tags"""

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save() method"""
        # If slug is not set, generate from title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# Create your models here.
class Post(models.Model):
    """Model for posts"""

    DRAFT = "draft"
    SCHEDULE = "schedule"
    PUBLISH = "publish"

    POST_STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (SCHEDULE, "Schedule"),
        (PUBLISH, "Publish"),
    ]

    title = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    body = QuillField("body")
    tags = models.ManyToManyField(Tag)
    featured_image = models.ImageField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=8, choices=POST_STATUS_CHOICES, default=DRAFT)
    publish_date = models.DateTimeField(blank=True, null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save method"""

        # If slug is not set, generate from title
        if not self.slug:
            self.slug = slugify(self.title)

        # Check if post status is set to publish and update publish_date
        if self.status == self.PUBLISH and not self.publish_date:
            self.publish_date = timezone.now()
        elif self.status == self.DRAFT and self.publish_date:
            self.publish_date = None
        elif self.publish_date is not None and self.publish_date > timezone.now():
            self.status = self.SCHEDULE
        elif self.status == self.SCHEDULE and self.publish_date <= timezone.now():
            self.status = self.PUBLISH

        # save the post
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-publish_date"]
