from .base import *
import os,sys

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'erp',
        'USER':     'postgres',
        'PASSWORD': 'admin@#$123',
        'HOST':     'localhost',
        'PORT':     5432,
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = PROJECT_DIR.child("collected_static")
STATICFILES_DIRS = (
    PROJECT_APPS.child("static"),
)

MEDIA_ROOT = PROJECT_APPS.child("media")
MEDIA_URL = '/media/'




FROM_EMAIL='arpitgupta0907.ag@gmail.com'
DEFAULT_FROM_EMAIL = 'arpitgupta0907.ag@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'arpitgupta0907.ag@gmail.com'
EMAIL_HOST_PASSWORD = 'bbqqscliowazatnc'
EMAIL_PORT = 587