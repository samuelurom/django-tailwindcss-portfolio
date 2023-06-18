from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, Tag
from main.models import SiteSettings, PageSettings

import math


# Create your views here.
def blog(request):
    posts = Post.objects.only(
        "title", "slug", "description", "publish_date", "featured_image"
    ).all()
    settings = SiteSettings.objects.first()
    page_info = PageSettings.objects.only(
        "blog_archive_title", "blog_archive_description"
    ).first()
    context = {"posts": posts, "settings": settings, "page_info": page_info}
    return render(request, "blog/blog.html", context)


def post(request, slug):
    # Get the post with slug
    post = get_object_or_404(Post, slug=slug)

    # Get number of words in post
    num_words = len(post.body.html.split())

    # Get read time in mins = num_words / 265 -> Average reading time is 265 WPM
    # value is rounded up
    readtime_mins = math.ceil(num_words / 265)

    settings = SiteSettings.objects.first()
    context = {"post": post, "readtime": readtime_mins, "settings": settings}
    return render(request, "blog/post.html", context)


def tag(request, slug):
    settings = SiteSettings.objects.first()

    tag = get_object_or_404(Tag, slug=slug)

    tag_archive = get_list_or_404(tag.post_set)

    print(tag_archive)

    context = {"tag": tag, "posts": tag_archive, "settings": settings}
    return render(request, "blog/tag.html", context)
