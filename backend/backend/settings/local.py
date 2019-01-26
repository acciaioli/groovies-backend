from .base import *  # noqa: F403 F401


DEBUG = True

INSTALLED_APPS.append('django_extensions')  # noqa: F405

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

ENV = 'dev'
