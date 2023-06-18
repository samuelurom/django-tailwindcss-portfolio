from django.urls import path

from . import views

# URLconf
urlpatterns = [
    path("", views.projects, name="projects"),
    path("<str:slug>/", views.project, name="project"),
]
