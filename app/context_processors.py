from .models import Photo, Blog


def global_context(request):
    photo_list = Photo.objects.all()
    blog_list = Blog.objects.all()
    return {
        "photo_list": photo_list,
        "blog_list": blog_list,
    }
