from django.db import models

from .managers import MovieManager


class Movie(models.Model):
    objects = MovieManager()

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
