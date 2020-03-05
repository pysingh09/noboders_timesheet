from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "thoughtwin_erp",
        "USER": "ashutosh",
        "PASSWORD": "adminadmin",
        "HOST": "localhost",
        "PORT": 5432,
    }
}

# local settings
try:
    from .local import *
except ImportError:
    pass
