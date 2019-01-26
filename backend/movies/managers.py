from django.db import models


class MovieQuerySet(models.QuerySet):
    def unrated(self, user):
        return self.exclude(ratings__user=user)
