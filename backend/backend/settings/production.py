from .base import *  # noqa: F403


DEBUG = False

INSTALLED_APPS.append('gunicorn')  # noqa: F405

ALLOWED_HOSTS = ["*"]
