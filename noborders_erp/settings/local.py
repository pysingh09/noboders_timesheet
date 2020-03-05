from .base import *


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


# EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
# FROM_EMAIL='ytiwari212@gmail.com'
# EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
# ANYMAIL = {

#     "SENDINBLUE_API_KEY": "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",
# }


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# FROM_EMAIL='erp.thoughtwin@gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = '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'
# EMAIL_PORT = 587

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# FROM_EMAIL='erp.thoughtwin@gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = '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'
# EMAIL_PORT = 587

FROM_EMAIL = "erp.thoughtwin@gmail.com"
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = 'AKIAQYKYEQYHWH555FXN'
# AWS_SECRET_ACCESS_KEY = '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'

# EMAIL_HOST_USER = 'AKIAQYKYEQYH2D47MJSN'
# EMAIL_HOST_PASSWORD = 'BAcOL3xrj69nRiRw0ncjvnYPkAhotCdgvh5qy7igQ6UX'
# EMAIL_PORT = 465
# EMAIL_USE_TLS = True
