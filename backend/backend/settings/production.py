import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *  # noqa: F403

sentry_sdk.init(
    dsn="https://1d8bbff6d60745e699e2931faf7bb461@sentry.io/1448752",
    integrations=[DjangoIntegration()]
)

DEBUG = False

INSTALLED_APPS.append('gunicorn')  # noqa: F405

ALLOWED_HOSTS = ["*"]

ENV = 'prod'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format':
                '[DJANGO] %(levelname)s %(asctime)s %(module)s %(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '*': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}
