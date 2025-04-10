from .models import Photo, Blog
from django.core.paginator import Paginator


def global_context(request):
    photos = Photo.objects.all()
    paginator = Paginator(photos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return {
        "photo": page_obj,
    }
