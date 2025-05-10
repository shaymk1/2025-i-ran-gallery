from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from core.settings.base import MEDIA_ROOT

urlpatterns = [
    #path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path(
        "secure-dashboard-2025/", admin.site.urls
    ),  # admin site url changed to "secure-dashboard-2025"
    
    path("", include("app.urls")),
]


# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
