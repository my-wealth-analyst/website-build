from .settings import *

DEBUG = False

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_HOST_USER = 'dean@mywealthanalyst.com'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = 'mywe@1th@n@1yst'
# EMAIL_PORT = 587
# EMAIL_USE_SSL = False
# EMAIL_USE_TLS = True


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "Mywealthanalyst <noreply@mywealthanalyst.com>"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = "[Mywealthanalyst]"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://sendgrid.com/docs/for-developers/sending-email/django/
# TODO Remove Ram's personal API key and replace with Menda's
SENDGRID_API_KEY = "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"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
