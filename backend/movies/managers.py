from django.db import models


class MovieManager(models.Manager):
    use_in_migrations = True
