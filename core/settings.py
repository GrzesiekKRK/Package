import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-1ihyyoz%jpb13h@6t%@c#d)6e4=1k5dhwyxt@pflt8&ql=xd%f'
DEBUG = bool(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangoql",
    "debug_toolbar",
    "django_extensions",
    "crispy_forms",
    "crispy_bootstrap4",
]

INSTALLED_EXTENSIONS = [
    "cargos",
    "notifications",
    "schedules",
    "users",
    "vehicles",
]

INSTALLED_APPS += INSTALLED_EXTENSIONS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",


]

ROOT_URLCONF = "core.urls"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
                # 'ENGINE': 'django.db.backends.postgresql',
                # 'NAME': BASE_DIR / 'Extra_package',
                # 'USER': 'postgres',
                # 'PASSWORD': '9261',
                # 'HOST': 'http://localhost:8000',
                # 'PORT': '5432',
    }
}


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "assets")


MEDIA_URL = "media/uploads/product/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.CustomUser"

LOGIN_REDIRECT_URL = "/login"
INTERNAL_IPS = [
    "127.0.0.1",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

SITE_URL = "http://localhost:8000"
