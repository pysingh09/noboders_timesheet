from .base import *
import os,sys

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'erpthoughtwin',
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


FROM_EMAIL='ankita@thoughtwin.com'
DEFAULT_FROM_EMAIL = 'ankita@thoughtwin.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587