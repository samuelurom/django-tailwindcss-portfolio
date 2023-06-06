from django.db import models


# Create your models here.
class Post(models.Model):
    DRAFT = 0
    PUBLISH = 1

    POST_STATUS = [(PUBLISH, "Publish"), (DRAFT, "Draft")]

    title = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    content = models.TextField()
    featured_image_path = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=POST_STATUS, default=DRAFT)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, created on {self.created_date}"
