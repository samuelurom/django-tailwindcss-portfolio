from django.shortcuts import render
from .models import SiteSettings, PageSettings, Work
from blog.models import Post
from project.models import Project


# Create your views here.
def home(request):
    posts = Post.objects.filter(status="publish")[:3]
    projects = Project.objects.filter(featured=True)[:3]

    settings = SiteSettings.objects.first()

    context = {"posts": posts, "settings": settings, "projects": projects}
    return render(request, "main/home.html", context)


def about(request):
    settings = SiteSettings.objects.first()
    page_info = PageSettings.objects.only(
        "about_page_image",
        "about_page_title",
        "about_page_description",
        "full_bio",
        "resume",
    ).first()
    work_experiences = Work.objects.all()

    context = {
        "settings": settings,
        "page_info": page_info,
        "work_experiences": work_experiences,
    }
    return render(request, "main/about.html", context)


def contact(request):
    settings = SiteSettings.objects.first()
    page_info = PageSettings.objects.only(
        "contact_page_title", "contact_page_description"
    ).first()

    context = {"settings": settings, "page_info": page_info}
    return render(request, "main/contact.html", context)
