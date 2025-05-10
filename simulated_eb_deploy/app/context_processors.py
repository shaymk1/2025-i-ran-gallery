from .models import Photo, Blog
from django.core.paginator import Paginator


def global_context(request):
    # Pagination for photos
    photos = Photo.objects.all()
    photo_paginator = Paginator(photos, 6) 
    photo_page_number = request.GET.get(
        "photo_page"
    )  # unique query parameter for photos
    photo_page_obj = photo_paginator.get_page(photo_page_number)

    # Pagination for blogs

    blogs = Blog.objects.all()
    blog_paginator = Paginator(blogs, 6)
    blog_page_number = request.GET.get("blog_page")
    blog_page_obj = blog_paginator.get_page(blog_page_number)
    return {
        "photo": photo_page_obj,  # Paginated photos
        "blog": blog_page_obj,  # Paginated blogs
    }
