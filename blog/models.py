from django.db import models
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    """Model for posts"""

    DRAFT = 0
    PUBLISH = 1

    POST_STATUS = [(PUBLISH, "Publish"), (DRAFT, "Draft")]

    title = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=1, choices=POST_STATUS, default=DRAFT)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override the save method"""
        # If slug is not set, generate from title
        if not self.slug:
            self.slug = slugify(self.title)

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
