import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework_jwt.settings import api_settings
from .managers import UserManager


def get_default_uuid():
    return uuid.uuid4().hex


class User(AbstractBaseUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    USERNAME_MAX_LEN = 30

    uuid = models.CharField(
        max_length=32,
        editable=False,
        null=False,
        blank=False,
        unique=True,
        default=get_default_uuid
    )

    email = models.EmailField(
        blank=False,
        null=False,
        unique=True
    )

    name = models.CharField(
        blank=False,
        null=False,
        max_length=20
    )

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def create_jwt(self) -> str:
        payload = api_settings.JWT_PAYLOAD_HANDLER(self)
        return api_settings.JWT_ENCODE_HANDLER(payload)
