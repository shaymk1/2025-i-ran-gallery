# from re import A
from calendar import c
import re
from django.shortcuts import render, redirect
from .models import Photo, Category, About, Blog
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404


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


def blog(request):
    # Fetch all blog posts for the main blog content
    blogs = Blog.objects.all().order_by("-date_created")

    # Add pagination logic
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Handle "Show All" logic for the blog titles list
    show_all_titles = request.GET.get("show_all_titles", "false").lower() == "true"
    if show_all_titles:
        blog_titles = Blog.objects.all().order_by("-date_created")
        # Show all blog titles
    else:
        blog_titles = Blog.objects.all().order_by("-date_created")[:5]
    # Show only the latest 5 titles # Show only the latest 5 titles

    context = {
        "blogs": page_obj,
        "blog_titles": blog_titles,  # Blog titles list
        "show_all_titles": show_all_titles,  # State for the "Show All" button
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


def add_blog(request):

    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")
        title = data.get("title")
        content = data.get("content")

        if image:
            Blog.objects.create(
                title=title,
                content=content,
                image=image,
            )

        else:
            Blog.objects.create(
                title=title,
                content=content,
            )

        return redirect("blog")
    context = {}
    return render(request, "add_blog.html", context)


# delete both blog and photo objects dynamically
def delete(request, object_type, id):

    # Determine the model based on the object_type
    if object_type == "photo":
        model = Photo
        redirect_url = "home"
    elif object_type == "blog":
        model = Blog
        redirect_url = "blog"
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
        return redirect(redirect_url)  # Redirect to home or another page after deletion

    # Render the delete confirmation page
    context = {
        "object": obj,
        "object_type": object_type,
    }
    return render(request, "delete.html", context)


# Update both blog and photo objects dynamically
def update(request, object_type, id):
    # Determine the model based on the object_type
    if object_type == "photo":
        model = Photo
        template_name = "update_photo.html"
        categories = Category.objects.all()
    elif object_type == "blog":
        model = Blog
        template_name = "update_blog.html"
        categories = None
    else:
        raise Http404("Invalid object type")

    obj = get_object_or_404(model, id=id)
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("image")
        title = data.get("title")
        content = data.get("content")
        content = data.get("content") if object_type == "blog" else None
        category_id = data.get("category") if object_type == "photo" else None

        # Update the object fields
        obj.title = title
        if object_type == "photo" and image:
            obj.image = image
        if object_type == "blog":
            obj.content = content
            if image:
                obj.image = image
        if object_type == "photo" and category_id != "none":
            obj.category = Category.objects.get(id=category_id)
        elif object_type == "photo":
            obj.category = None

        obj.save()
        return redirect("home" if object_type == "photo" else "blog")

    context = {
        "object": obj,
        "object_type": object_type,
        "categories": categories,
    }
    return render(request, template_name, context)


# edit category for photo object
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        data = request.POST
        category.month = data.get("month")
        category.venue = data.get("venue")
        category.race = data.get("race")
        category.save()
        return redirect("home")  # Redirect to the home page or another relevant page

    context = {
        "category": category,
    }
    return render(request, "edit_category.html", context)


def about(request):
    about = About.objects.all()
    context = {
        "about": about,
    }
    return render(request, "about.html", context)
