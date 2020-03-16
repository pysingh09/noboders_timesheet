"""
Django settings for noborders_erp project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os, sys
from decouple import config
from dj_database_url import parse as dburl

# setting ---------------------------------------------------------
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = Path(__file__).ancestor(3)
PROJECT_APPS = Path(__file__).ancestor(2)

sys.path.insert(0, Path(PROJECT_APPS, "apps"))
# ------------------------------------------------------------------

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "b6ehjxx)la#yrzhlt$e!+to=$p$#%uz4coa!0*9bxeu9w&-zm0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "django_filters",
    "django_extensions",
    "employee",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "employee.middleware.AuthRequiredMiddleware",  # before login redirection
]

ROOT_URLCONF = "noborders_erp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_APPS.child("templates"),],
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

WSGI_APPLICATION = "noborders_erp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# settings.py

AUTHENTICATION_BACKENDS = (
    "noborders_erp.apps.employee.auth_email_backend.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "/"

# https://docs.djangoproject.com/en/2.0/howto/static-files/
# media files (Pdf, Images)
MEDIA_ROOT = PROJECT_APPS.child("media")

MEDIA_URL = "/media/"

# Static files (CSS, JavaScript, Images, Pdf)
STATIC_ROOT = PROJECT_APPS.child("staticfiles")

STATIC_URL = "/staticfiles/"

STATICFILES_DIRS = [
    PROJECT_APPS.child("static"),
]

AUTH_USER_EMAIL_UNIQUE = True

# CRISPY_TEMPLATE_PACK = 'bootstrap4'
# =======


LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    "/admin",
    "/login",
    "/forgot-password",
)


# celery settings
# CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# CELERY_TIMEZONE = 'Asia/Kolkata'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'


BROKER_URL = "amqp://localhost"
CELERY_RESULT_BACKEND = "rpc://"
CELERY_RESULT_PERSISTENT = False
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"