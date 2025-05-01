from django.shortcuts import render, redirect
from .models import Photo, Category, About, Blog
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from .forms import BlogForm, UpdateBlogForm, UpdatePhotoForm, ContactForm, SubscribeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.mail import send_mail
import sib_api_v3_sdk  # for sending emails using sendinblue
from sib_api_v3_sdk.rest import ApiException  # for sending emails using sendinblue
from django.conf import settings

#####################photo views#######################


def home(request):
    photos = Photo.objects.all()
    category = Category.objects.all()
    tags = Blog.objects.filter(tags__name__in=["name"]).distinct()
    paginator = Paginator(photos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "photo": page_obj,
        "category": category,
        "tags": tags,
    }

    return render(request, "index.html", context)


def photo_detail(request, id):
    photo = Photo.objects.get(id=id)
    context = {
        "photo": photo,
    }
    return render(request, "photo_detailed.html", context)


@login_required(login_url="login")
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
        messages.success(request, "photo added successfully!")
        return redirect("home")

    context = {
        "category": category,
        "photo": photo,
    }

    return render(request, "add_photo.html", context)


# update jsut the photo object
@login_required(login_url="login")
def update_photo(request, id):
    photo = get_object_or_404(Photo, id=id)
    category = Category.objects.all()
    if request.method == "POST":
        form = UpdatePhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, "photo updated successfully!")
            return redirect("home")
        else:
            messages.error(request, "Something went wrong, please try again...")
    else:
        form = UpdatePhotoForm(instance=photo)
    context = {
        "form": form,
        "category": category,
        "photo": photo,
    }
    return render(request, "update_photo.html", context)


#####################blog views#######################


def blog(request):
    # Fetch all blog posts for the main blog content
    blogs = Blog.objects.all().order_by("-date_created")
    # Fetch tags by name
    tags = Blog.objects.filter(tags__name__in=["name"]).distinct()
    # Fetch all tags
    all_tags = Tag.objects.all()
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
        "show_all_titles": show_all_titles,
        "tags": tags,  # Tags by name
        "all_tags": all_tags,  # All tags
    }
    return render(request, "blog.html", context)


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    photo = Photo.objects.all()
    # Get tags for the current blog
    blog_tags = blog.tags.all()
    # Find other blogs that share at least one tag with the current blog, excluding itself
    related_posts = (
        Blog.objects.filter(tags__in=blog_tags).exclude(id=blog.id).distinct()[:4]
    )
    context = {
        "blog": blog,
        "photo": photo,
        "related_posts": related_posts,
        "blog_tags": blog_tags,
    }
    return render(request, "blog_detailed.html", context)


@login_required(login_url="login")
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post created successfully!")
            return redirect("blog")
        else:
            messages.error(request, "Something went wrong, please try again...")
    else:
        form = BlogForm()

    context = {"form": form}
    return render(request, "add_blog.html", context)


# update just the blog
@login_required(login_url="login")
def update_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        form = UpdateBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully!")
            return redirect("blog")
        else:
            messages.error(request, "Something went wrong, please try again...")

    else:
        form = UpdateBlogForm(instance=blog)

    context = {
        "object": blog,
        "form": form,
    }
    return render(request, "update_blog.html", context)


# tags for blogs
def blog_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    blogs = Blog.objects.filter(tags__in=[tag])
    return render(request, "blog.html", {"blogs": blogs})


#####################Delete views#######################


# delete both blog and photo objects dynamically
@login_required(login_url="login")
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
        messages.success(request, f"{object_type.capitalize()} deleted successfully.")
        return redirect(redirect_url)

    # Render the delete confirmation page
    context = {
        "object": obj,
        "object_type": object_type,
    }
    return render(request, "delete.html", context)


#####################login and logout messages#######################


def login_with_message(request):
    if request.user.is_authenticated:
        return redirect("home")
    response = LoginView.as_view(template_name="registration/login.html")(request)
    if request.method == "POST" and request.user.is_authenticated:
        messages.success(request, f"Welcome back, {request.user.username}!")
    return response


def logout_with_message(request):
    messages.success(request, "You have been logged out successfully.")
    return LogoutView.as_view(next_page="home")(request)
    # return redirect("home")


#####################contact#######################


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            send_mail(
                f"Contact Form: {form.cleaned_data['name']}",
                form.cleaned_data["message"],
                form.cleaned_data["email"],
                ["shaesblog12@gmail.com"],
            )
            messages.success(request, "Your message has been sent!")
            form = ContactForm()  # Clear the form
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


#####################subscribe views with sdk and brevo#######################


def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            config = sib_api_v3_sdk.Configuration()
            api_key = settings.BREVO_API_KEY
            # config.api_key["api-key"] = settings.BREVO_API_KEY
            api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(config))
            try:
                # check if contact exists
                api_instance.get_contact_info(email)  # Will raise 404 if not found
                messages.info(request, "You're already subscribed!")
            except ApiException as e:
                if e.status == 404:
                    # Only proceed if email is new
                    create_contact = sib_api_v3_sdk.CreateContact(
                        email=email, list_ids=[2], update_enabled=True
                    )
                    api_instance.create_contact(create_contact)
                    messages.success(request, "Thanks for subscribing!")
                else:
                    messages.error(
                        request, "Subscription service unavailable. Try again later."
                    )
                if messages.success:
                    return render(request, "subscribe_success.html", {"no_base": True})
                else:
                    return render(request, "subscribe_error.html", {"no_base": True})
            return redirect("home")
    else:
        form = SubscribeForm()
    context = {
        "form": form,
        "api_key": api_key,
    }
    return render(request, "subscribe.html", context)


# Update both blog and photo objects dynamically
# def update(request, object_type, id):
#     # Determine the model based on the object_type
#     if object_type == "photo":
#         model = Photo
#         template_name = "update_photo.html"
#         categories = Category.objects.all()
#     elif object_type == "blog":
#         model = Blog
#         template_name = "update_blog.html"
#         categories = None
#     else:
#         raise Http404("Invalid object type")

#     obj = get_object_or_404(model, id=id)
#     if request.method == "POST":
#         data = request.POST
#         image = request.FILES.get("image")
#         title = data.get("title")
#         content = data.get("content")
#         content = data.get("content") if object_type == "blog" else None
#         category_id = data.get("category") if object_type == "photo" else None

#         # Update the object fields
#         obj.title = title
#         if object_type == "photo" and image:
#             obj.image = image
#         if object_type == "blog":
#             obj.content = content
#             if image:
#                 obj.image = image
#         if object_type == "photo" and category_id != "none":
#             obj.category = Category.objects.get(id=category_id)
#         elif object_type == "photo":
#             obj.category = None

#         obj.save()
#         return redirect("home" if object_type == "photo" else "blog")

#     context = {
#         "object": obj,
#         "object_type": object_type,
#         "categories": categories,
#     }
#     return render(request, template_name, context)


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


def search(request):
    query = request.GET.get("q", "")
    results = []
    # for photos
    photo_results = Photo.objects.filter(
        Q(title__icontains=query)
        | Q(category__month__icontains=query)
        | Q(category__venue__icontains=query)
        | Q(category__race__icontains=query)
    )
    # for blogs
    blog_results = Blog.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    # Combine results
    results = list(photo_results) + list(blog_results)

    context = {
        "photo_results": photo_results,
        "blog_results": blog_results,
        "query": query,
        "results": results,
    }
    return render(request, "search.html", context)


# # incase my about data is not in the database, i can add it manually in the front end
# def add_about(request):
#     if request.method == "POST":
#         form = AboutForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("about")
#     else:
#         form = AboutForm()

#     context = {
#         "form": form,
#     }
#     return render(request, "add_about.html", context)


# another way of adding a blog in the front end
# if request.method == "POST":
#     data = request.POST
#     image = request.FILES.get("image")
#     title = data.get("title")
#     content = data.get("content")

#     if image:
#         Blog.objects.create(
#             title=title,
#             content=content,
#             image=image,
#         )

#     else:
#         Blog.objects.create(
#             title=title,
#             content=content,
#         )

# return redirect("blog")
