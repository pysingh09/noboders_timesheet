import dj_database_url
from .base import *
import os,sys

DEBUG = False

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'hobby-dev',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }


SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [PROJECT_ROOT.split("/settings")[0] + "/static"]

# STATIC_URL = '/static/'
# STATIC_ROOT = PROJECT_DIR.child("collected_static")
# STATICFILES_DIRS = (
#     PROJECT_APPS.child("static"),
# )

# MEDIA_ROOT = PROJECT_APPS.child("media")
# MEDIA_URL = '/media/'


# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# FROM_EMAIL='rathoreutkarsh0699@gmail.com'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = 'AKIAQYKYEQYHWH555FXN'
# AWS_SECRET_ACCESS_KEY = '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'



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
