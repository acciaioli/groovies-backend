from django.db import models

from .managers import MovieQuerySet


class Movie(models.Model):
    objects = MovieQuerySet.as_manager()

    title = models.CharField(
        max_length=100,
        default=None,
        null=False,
    )

    year = models.CharField(
        max_length=4,
        default=None,
        null=False,
    )

    description = models.TextField(
        default=None,
        null=True,
    )

    url = models.URLField(
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
