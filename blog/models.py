from django.db import models
from django.utils.text import slugify
from django.utils import timezone


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
    body = models.TextField()
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
        elif self.publish_date > timezone.now():
            self.status = self.SCHEDULE
        elif self.status == self.SCHEDULE and self.publish_date <= timezone.now():
            self.status = self.PUBLISH

        # save the post
        super().save(*args, **kwargs)


class Category(models.Model):
    """Model for categories"""

    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    description = models.TextField()

    class Meta:
        # Customize the display name in plural
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override save() method"""
        # If slug is not set, generate from title
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class CategorizedPost(models.Model):
    """What tag is applied to what post?"""

    tag = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Tag(models.Model):
    """Model for tags"""

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save() method"""
        # If slug is not set, generate from title
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TaggedPost(models.Model):
    """What tag is applied to what post?"""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
