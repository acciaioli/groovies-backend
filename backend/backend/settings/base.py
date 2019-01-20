import os
import datetime

from j_crypto import PemKeyLoader


# https://docs.djangoproject.com/en/2.1/ref/settings/#debug
DEBUG = False

# https://docs.djangoproject.com/en/2.1/ref/settings/#secret-key
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS: list = []

# https://docs.djangoproject.com/en/2.1/ref/settings/#root-urlconf
ROOT_URLCONF = 'backend.urls'

# https://docs.djangoproject.com/en/2.1/ref/settings/#wsgi-application
WSGI_APPLICATION = 'backend.wsgi.application'

# https://docs.djangoproject.com/en/2.1/ref/settings/#installed-apps
INSTALLED_APPS = [
    'rest_framework',  # utilities for rest apis
    'corsheaders',

    'users',
    'rooms',
    'movies'
]

# https://docs.djangoproject.com/en/2.0/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # https://github.com/ottoyiu/django-cors-headers
]

# https://docs.djangoproject.com/en/2.1/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = ['users.backends.EmailModelBackend']

# https://docs.djangoproject.com/en/2.1/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://docs.djangoproject.com/en/2.1/ref/settings/#admins
ADMINS = (
    ('Author', 'acci.valverde@gmail.com'),
)

# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    # ENGINE://USER:PASSWORD@HOST:PORT/NAME
    'default': {
        # https: // docs.djangoproject.com / en / 2.1 / ref / settings /  # engine
        'ENGINE': 'django.db.backends.postgresql',

        # https://docs.djangoproject.com/en/2.1/ref/settings/#user
        'USER': os.getenv('POSTGRES_USER'),

        # https://docs.djangoproject.com/en/2.1/ref/settings/#password
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),

        # https://docs.djangoproject.com/en/2.1/ref/settings/#host
        'HOST': os.getenv('POSTGRES_HOST'),

        # https://docs.djangoproject.com/en/2.1/ref/settings/#port
        'PORT': os.getenv('POSTGRES_PORT'),

        # https://docs.djangoproject.com/en/2.1/ref/settings/#name
        'NAME': os.getenv('POSTGRES_DB'),

        # https://docs.djangoproject.com/en/2.1/ref/settings/#conn-max-age
        'CONN_MAX_AGE': int(os.getenv('POSTGRES_CONN_MAX_AGE', '0'))
    },
}

# https://docs.djangoproject.com/en/2.1/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# https://docs.djangoproject.com/en/2.1/ref/settings/#time-zone
TIME_ZONE = None

# https://docs.djangoproject.com/en/2.1/ref/settings/#use-i18n
USE_I18N = False

# https://docs.djangoproject.com/en/2.1/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/2.1/ref/settings/#use-tz
USE_TZ = False

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    # https://www.django-rest-framework.org/api-guide/settings/#unauthenticated_user
    'UNAUTHENTICATED_USER': None,

    # https://www.django-rest-framework.org/api-guide/settings/#default_authentication_classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ],

    # https://www.django-rest-framework.org/api-guide/settings/#default_permission_classes
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # https://www.django-rest-framework.org/api-guide/settings/#default_renderer_classes
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],

    # https://www.django-rest-framework.org/api-guide/settings/#default_parser_classes
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],

    # https://www.django-rest-framework.org/api-guide/pagination/#setting-the-pagination-style
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # https://www.django-rest-framework.org/api-guide/settings/#page_size
    'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', '20')),

    # https://www.django-rest-framework.org/api-guide/settings/#datetime_format
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
}

# jwt private / public keys
# a private key is necessary if this service is responsible for generating JWTs
private_key = PemKeyLoader.load_private_key(os.getenv('DJANGO_JWT_PRIVATE_KEY', ''))
# a public key is necessary if this service needs to verify incoming JWTs
public_key = PemKeyLoader.load_public_key(os.getenv('DJANGO_JWT_PUBLIC_KEY', ''))

# enable if this service will be creating jwts
# assert private_key is not None, 'Private Key not found'

assert public_key is not None, 'Public Key not found'


# http://getblimp.github.io/django-rest-framework-jwt/#additional-settings
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_PRIVATE_KEY': private_key,
    'JWT_PUBLIC_KEY': public_key,
    'JWT_ALGORITHM': 'RS256'
}

# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'

# https://github.com/OttoYiu/django-cors-headers#cors_origin_allow_all
CORS_ORIGIN_ALLOW_ALL = True

# https://github.com/OttoYiu/django-cors-headers#cors_allow_methods
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

# https://github.com/OttoYiu/django-cors-headers#cors_allow_headers
CORS_ALLOW_HEADERS = (
    'authorization',
    'content-type',
)


# custom
START_DATETIME = datetime.datetime.now()
