from pathlib import Path
from dotenv import load_dotenv
import os
from django.urls import reverse_lazy  # for login redirect
import shutil
import dj_database_url  # for database config
#import logging

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Secret key & debug
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

ADMIN_URL = "secure-dashboard-2025/"

# Installed apps
INSTALLED_APPS = [
    "app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "taggit",
    "imagekit",
    "django.contrib.sitemaps",
]

SITE_ID = 1

# Middleware
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

ROOT_URLCONF = "core.urls"

LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("home")

# Session config
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_SECONDS = 1800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_FILE_PATH = os.path.join(BASE_DIR, "sessions")
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_TIMEOUT_REDIRECT = "home"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.global_context",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Fly.io/Postgres database config
# DATABASES = {
#     "default": dj_database_url.config(default="sqlite:///db.sqlite3", conn_max_age=600)
# }
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'),  # Reads from Fly.io's environment
#         conn_max_age=600,  # Optional: improves performance
#         ssl_require=not DEBUG,   # Important for production!
#     )
# }

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=False  # not needed for SQLite
    )
}

# Email (Gmail example)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

DOMAIN = "localhost:8000" if DEBUG else "your-app.fly.dev"
PROTOCOL = "http" if DEBUG else "https"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# i18n
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (local)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files (local)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Production security
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "django.log",
            "level": "INFO",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}

# Clear session files on startup (if file backend ever used again)
if SESSION_ENGINE.endswith("file"):
    session_dir = SESSION_FILE_PATH
    if session_dir and os.path.exists(session_dir):
        try:
            shutil.rmtree(session_dir)
            os.makedirs(session_dir, exist_ok=True)
        except Exception as e:
            print(f"Couldn't clear session dir: {e}")
