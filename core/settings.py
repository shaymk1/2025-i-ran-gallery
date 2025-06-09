from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url  # for database config

# import shutil  # for clearing session files
# from django.urls import reverse_lazy

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")
# Set DEBUG from environment first, so we know if we should load .env
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Secret key & debug
SECRET_KEY = os.environ.get("SECRET_KEY")
#DOMAIN = "in-2025-i-ran-blog.fly.dev"  # from fly.io
# Set ALLOWED_HOSTS from environment or default for production
ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS", "localhost,127.0.0.1,in-2025-i-ran-blog.fly.dev"
).split(",")
ADMIN_URL = "secure-dashboard-2025/"

# Django requires ROOT_URLCONF to be set
ROOT_URLCONF = "core.urls"

# Application definition
INSTALLED_APPS = [
    "app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # for django-allauth
    # "storages",  # aws s3
    "taggit",  # for tags
    "imagekit",  # for image optimization
    "django.contrib.sitemaps",  # for sitemaps
    # "admin_honeypot",  # for honeypot
    # "cloudinary",
    # "cloudinary_storage",
]

# Fly.io/Postgres database config
# DATABASES = {
#     "default": dj_database_url.config(
#         default=os.environ.get("DATABASE_URL"),
#         conn_max_age=600,
#         ssl_require=not DEBUG,  # Require SSL in production
#     )
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# ImageKit settings
IMAGEKIT_CACHEFILE_DIR = 'CACHE/images'
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
# Comment out cloudinary config for now since we're running locally
# cloudinary config
# DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
# CLOUDINARY_STORAGE = {
#     "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
#     "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
#     "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
# }
SITE_ID = 1  # for django-allauth

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR / "app" / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.media',  
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.global_context",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Static and media files configuration for Fly.io
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Optionally, if using Whitenoise for static files in production:
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging Configuration for s3
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "django.log",  # Log file path
            "level": "INFO",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],  # Log to both console and file
            "level": "INFO",
        },
        "boto3": {
            "handlers": ["console", "file"],
            "level": "WARNING",
        },
        "botocore": {
            "handlers": ["console", "file"],
            "level": "WARNING",
        },
    },
}
