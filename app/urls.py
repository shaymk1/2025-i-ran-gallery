from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
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
    # to reset password
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset_form.html",
            email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
