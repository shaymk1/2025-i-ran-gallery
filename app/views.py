# from re import A
from calendar import c
from django.shortcuts import render
from .models import Photo, Category, About, Blog


def home(request):
    photos = Photo.objects.all()
    category = Category.objects.all()
    context = {
        "photo": photos,
        "category": category,
        # "photo_list": photos,
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
        # "blog_list": blogs,
    }
    return render(request, "blog.html", context)


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    photo = Photo.objects.all()
    category = blog.categories.all()
    context = {
        "blog": blog,
        "photo": photo,
        "category": category,
    }
    return render(request, "blog_detailed.html", context)


def photo_detail(request, id):
    photo = Photo.objects.get(id=id)
    context = {
        "photo": photo,
    }
    return render(request, "photo_detailed.html", context)


def add_photo(request):
    category = Category.objects.all()
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")
        if data[category] != "none":
            category = Category.objects.get(id=data["category"])
        elif data["category_new"] == "":
            data, created = Category.objects.get_or_create(name=data["category_new"])
        else:
            category = None
        # save the photo object
        photo = Photo.objects.create(
            title=data["title"],
            image=image,
            category=category,
        )
    context = {
        "category": category,
        "photo": photo,
    }

    return render(request, "add_photo.html", context)


# def blog_by_category(request, slug):
#     category = Category.objects.filter(slug=slug).first()
#     if not category:
#         return render(request, "404.html")
#     blog = Blog.objects.get(slug=slug)
#     photo = Photo.objects.all()
#     context = {
#         "blog": blog,
#         "category": category,
#         "photo": photo,
#     }
#     return render(request, "blog_by_category.html", context)
