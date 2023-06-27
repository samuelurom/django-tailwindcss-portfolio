from datetime import datetime
from django.db import models
from django_quill.fields import QuillField

# Create your models here.


class SiteSettings(models.Model):
    SETTING_TYPE = "site-settings"

    SETTING_CHOICES = [(SETTING_TYPE, "site-settings")]

    setting_type = models.CharField(
        primary_key=True, max_length=13, choices=SETTING_CHOICES, default=SETTING_TYPE
    )
    profile_image = models.ImageField(max_length=255, null=True, blank=True)
    icon = models.ImageField(max_length=255, null=True, blank=True)
    site_title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    short_bio = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    footer_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Settings: {self.site_title} - {self.subtitle}"

    class Meta:
        verbose_name_plural = "Site settings"


class PageSettings(models.Model):
    SETTING_TYPE = "page-settings"

    SETTING_CHOICES = [(SETTING_TYPE, "page-settings")]

    # Set setting_type as primary key with only "page setting" as input
    # To ensure only one record is entered in table

    setting_type = models.CharField(
        primary_key=True, max_length=13, choices=SETTING_CHOICES, default=SETTING_TYPE
    )

    resume = models.FileField(max_length=255, null=True, blank=True)
    about_page_image = models.ImageField(max_length=255, null=True, blank=True)
    about_page_title = models.CharField(max_length=255, null=True, blank=True)
    about_page_subtitle = models.CharField(max_length=255, null=True, blank=True)
    about_page_description = models.CharField(max_length=255, null=True, blank=True)
    full_bio = QuillField(null=True, blank=True)
    experience_subtitle = models.CharField(max_length=255, null=True, blank=True)
    experience_description = models.CharField(max_length=255, null=True, blank=True)
    projects_archive_title = models.CharField(max_length=255, null=True, blank=True)
    projects_archive_description = models.CharField(
        max_length=255, null=True, blank=True
    )
    blog_archive_title = models.CharField(max_length=255, null=True, blank=True)
    blog_archive_description = models.CharField(max_length=255, null=True, blank=True)
    contact_page_title = models.CharField(max_length=255, null=True, blank=True)
    contact_page_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Settings: Page Settings"

    class Meta:
        verbose_name_plural = "Page settings"


class Work(models.Model):
    YEAR_CHOICES = [(None, None)]

    # Get years from 1980 to present
    for year in range(1980, datetime.now().year + 1):
        YEAR_CHOICES.append((year, year))

    company_logo = models.ImageField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_year = models.IntegerField(choices=YEAR_CHOICES)
    end_year = models.IntegerField(choices=YEAR_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.company_name}, {self.role} ({self.start_year} - {self.end_year})"

    class Meta:
        ordering = ["-start_year"]
