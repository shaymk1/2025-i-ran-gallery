from django.apps import AppConfig
# import cloudinary
# from decouple import config


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    # to delay cloudinary config until the app is ready
    # def ready(self):
    #     cloudinary.config(secure=True, cloudinary_url=config("CLOUDINARY_URL"))
