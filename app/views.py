from re import A
from django.shortcuts import render
from .models import Photo, Category, About, Blog


def home(request):
    photos = Photo.objects.all()
    category = Category.objects.all()
    context = {
        "photo": photos,
        "category": category,
    }
    return render(request, "index.html", context)


def about(request):
    about = About.objects.all()
    context = {
        "about": about,
    }
    return render(request, "about.html", context)


def blog(request):
    blogs = Blog.objects.all()
    context = {
        "blogs": blogs,
    }
    return render(request, "blog.html", context)
