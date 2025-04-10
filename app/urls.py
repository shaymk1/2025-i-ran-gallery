from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("photo/<int:id>/", views.photo_detail, name="photo_detail"),
    path("add_photo/", views.add_photo, name="add_photo"),
    path("delete/<str:object_type>/<int:id>/", views.delete, name="delete"),
    # path("add_blog/", views.add_blog, name="add_blog"),
    # path("blog/<slug:slug>/", views.blog_by_category, name="blog_by_category"),
]
