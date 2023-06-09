from django.db import models


# Create your models here.
class Post(models.Model):
    """Model for posts"""

    DRAFT = 0
    PUBLISH = 1

    POST_STATUS = [(PUBLISH, "Publish"), (DRAFT, "Draft")]

    title = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    content = models.TextField()
    featured_image = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=POST_STATUS, default=DRAFT)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """Model for categories"""

    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


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


class TaggedPost(models.Model):
    """What tag is applied to what post?"""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
