from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("photo/<int:id>/", views.photo_detail, name="photo_detail"),
    path("add_photo/", views.add_photo, name="add_photo"),
    path("delete/<str:object_type>/<int:id>/", views.delete, name="delete"),
    path("add_blog/", views.add_blog, name="add_blog"),
    path("update/<str:object_type>/<int:id>/", views.update, name="update"),
    path("edit_category/<int:id>/", views.edit_category, name="edit_category"),
    path("search/", views.search, name="search"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    # path('logout/', logout_then_login, name='logout'),
    # path("add_about/", views.add_about, name="add_about"),
]
