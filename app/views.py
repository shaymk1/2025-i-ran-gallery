
from django.shortcuts import render
from .models import Photo, Category


def home(request):
    photos = Photo.objects.all()
    category = Category.objects.all()
    context = {
        "photo": photos,
        "category": category,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def blog(request):
    return render(request, "blog.html")
