from pathlib import Path
from dotenv import load_dotenv
import os
from django.urls import reverse_lazy
import shutil  # for clearing session files
import logging  # for logging s3 errors


# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")

# brevo-api-key for email subscription
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")

"""
secret key
debug mode
- True for development
- False for production
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS", "localhost,127.0.0.1,.elasticbeanstalk.com"
).split(",")


# Disable boto3 debug logging
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)

# Application definition
INSTALLED_APPS = [
    "app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",  # aws s3
    "taggit",  # for tags
    "imagekit",  # for image optimization
    "django.contrib.sitemaps",  # for sitemaps
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

"""
Login Configuration
- Redirects to login page if not authenticated
- Redirects to home page after login
- Uses reverse_lazy to avoid circular imports
"""
LOGIN_URL = reverse_lazy("login")
LOGIN_REDIRECT_URL = reverse_lazy("home")

"""
Session Configuration
- Logs out when browser is closed
- Session cookie age (in seconds) if browser stays open
- Resets timeout on activity
- Path to store session files
- Clears all sessions on server restart (optional)
"""
# Logs out when browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#  Session cookie age (in seconds) if browser stays open
SESSION_COOKIE_AGE = 3600
# Resets timeout on activity
SESSION_SAVE_EVERY_REQUEST = True
SESSION_FILE_PATH = "C:\\tmp\\django_sessions"
# Path to store session files
SESSION_FILE_PATH = os.path.join(BASE_DIR, "sessions")
# Clears all sessions on server restart (optional)
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR / "app" / "templates"),
        ],
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
# DATABASES = {
#      'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#      }
#      }
# Email Configuration (Gmail example)smtp
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

if not DEBUG:
    DOMAIN = "yourdomain.com"  # For production
else:
    DOMAIN = "localhost:8000"  # For local testing
    PROTOCOL = "http"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


"""
aws s3 configuration
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY 
- AWS_STORAGE_BUCKET_NAME
"""
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "eu-north-1")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = "public-read"
AWS_S3_VERIFY = True
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}


"""
storage configuration
- Default storage backend for media files
- Static files storage backend
- Custom storage backend for media files
"""
# Storage Configuration s3
STORAGES = {
    "default": {
        "BACKEND": "core.custom_storage.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files (User uploads)
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security settings if not in debug mode
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

"""
# Clear session files on server startup
# if hasattr(settings, "SESSION_FILE_PATH"):  # Check if using file-based sessions
#     session_dir = settings.SESSION_FILE_PATH
 """
if SESSION_ENGINE.endswith("file"):
    session_dir = SESSION_FILE_PATH
    if session_dir and os.path.exists(session_dir):
        try:
            shutil.rmtree(session_dir)
            os.makedirs(session_dir, exist_ok=True)
        except Exception as e:
            print(f"Couldn't clear session dir: {e}")
# Clear session files on server startup
# if hasattr(settings, "SESSION_FILE_PATH"):  # Check if using file-based sessions
#     session_dir = settings.SESSION_FILE_PATH
#     if os.path.exists(session_dir):  # If session folder exists
#         shutil.rmtree(session_dir)  # Delete it and all session files inside
#     os.makedirs(session_dir, exist_ok=True)  # Recreate the folder
