from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
  'default': {
      'ENGINE':   'django.db.backends.postgresql',
      'NAME':     'thoughtwin_erp',
      'USER':     'postgres',
      'PASSWORD': 'psql',
      'HOST':     'localhost',
      'PORT':     5432,
  }
}

# local settings
try:
    from .local import *
except ImportError:
    pass