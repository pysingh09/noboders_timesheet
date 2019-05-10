from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_APPS.child("static"),
)

MEDIA_ROOT = PROJECT_APPS.child("media")
MEDIA_URL = '/media/'

# local settings
try:
    from .local import *
except ImportError:
    pass