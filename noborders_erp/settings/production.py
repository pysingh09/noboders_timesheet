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



FROM_EMAIL='rathoreutkarsh0699@gmail.com'
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAQYKYEQYHWH555FXN'
AWS_SECRET_ACCESS_KEY = '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'



# FROM_EMAIL='erp.thoughtwin@gmail.com'
# DEFAULT_FROM_EMAIL = 'erp.thoughtwin@gmail.com'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'erp.thoughtwin@gmail.com'
# EMAIL_HOST_PASSWORD = 'cuqtnmjcdregfyfd'



# EMAIL_HOST_USER = 'AKIAQYKYEQYH2D47MJSN'
# EMAIL_HOST_PASSWORD = 'BAcOL3xrj69nRiRw0ncjvnYPkAhotCdgvh5qy7igQ6UX'
# EMAIL_PORT = 465
# EMAIL_USE_TLS = True
