from django.contrib import admin
from .models import SiteSettings, PageSettings, Work

# Register your models here.

admin.site.register(SiteSettings)
admin.site.register(PageSettings)
admin.site.register(Work)
