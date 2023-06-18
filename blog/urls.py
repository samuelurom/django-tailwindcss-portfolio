from django.urls import path
from . import views

# URLconf
urlpatterns = [
    path("", views.blog, name="blog"),
    path("<str:slug>/", views.post, name="post"),
    path("tag/<str:slug>/", views.tag, name="tag"),
]
