from django.shortcuts import render
from main.models import SiteSettings, PageSettings
from .models import Project


# Create your views here.
def projects(request):
    settings = SiteSettings.objects.first()
    page = PageSettings.objects.only(
        "projects_archive_title", "projects_archive_description"
    ).first()
    projects = Project.objects.all()

    context = {"settings": settings, "page": page, "projects": projects}

    return render(request, "project/projects_archive.html", context)


def project(request, slug):
    settings = SiteSettings.objects.first()
    project = Project.objects.get(slug=slug)

    context = {"project": project, "settings": settings}

    return render(request, "project/project.html", context)
