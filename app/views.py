from re import A
from django.shortcuts import render
from .models import Photo, Category, About, Blog


def home(request):
    photos = Photo.objects.all()
    category = Category.objects.all()
    context = {
        "photo": photos,
        "category": category,
        "photo_list": photos,
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
        "blog_list": blogs,
    }
    return render(request, "blog.html", context)


def blog_detail(request, id):
    blog = Blog.objects.get(id=id)
    context = {
        "blog": blog,
    }
    return render(request, "blog_detail.html", context)


def photo_detail(request, id):
    photo = Photo.objects.get(id=id)
    context = {
        "photo": photo,
    }
    return render(request, "photo_detail.html", context)
