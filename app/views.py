# from re import A
from calendar import c
from django.shortcuts import render, redirect
from .models import Photo, Category, About, Blog
from django.core.paginator import Paginator
from django.http import Http404


def home(request):
    photos = Photo.objects.all()
    category = Category.objects.all()
    paginator = Paginator(photos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "photo": page_obj,
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
    photo = None
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")
        # category_title = data.get("category_title", "")
        category_month = data.get("category_month", "")
        category_venue = data.get("category_venue", "")
        category_race = data.get("category_race", "")
        # check if an existing category is selected
        if data.get("category") != "none":
            category = Category.objects.get(id=data.get("category"))
            # otherwise create a new category
        elif category_month and category_venue and category_race:
            category, created = Category.objects.get_or_create(
                # title=data["category_title"],
                month=category_month,
                venue=category_venue,
                race=category_race,
                defaults={
                    "slug": f"{category_month} -{category_venue}-{category_race}"
                },
            )
        else:
            category = None
            # save the Photo object if image is provided
        if image:
            photo = Photo.objects.create(
                title=data.get("title"),
                image=image,
                category=category,
            )

        return redirect("home")
    context = {
        "category": category,
        "photo": photo,
    }

    return render(request, "add_photo.html", context)


def delete(request, object_type, id):

    # Determine the model based on the object_type
    if object_type == "photo":
        model = Photo
    elif object_type == "blog":
        model = Blog
    else:
        raise Http404("Invalid object type")

    # Get the object to delete
    try:
        obj = model.objects.get(id=id)
    except model.DoesNotExist:
        raise Http404(f"{object_type.capitalize()} not found")
    # Handle POST request to confirm deletion
    if request.method == "POST":
        obj.delete()
        return redirect("home")  # Redirect to home or another page after deletion

    # Render the delete confirmation page
    context = {
        "object": obj,
        "object_type": object_type,
    }
    return render(request, "delete.html", context)
