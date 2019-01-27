from django.db import models, IntegrityError

from ml_proxy import get_proxy
from . import constants
from .exceptions import RoomUsersNotReady
from .managers import RoomManager


class Room(models.Model):
    objects = RoomManager()

    slug = models.SlugField(
        max_length=20,
        unique=True,
        null=False,
        default=None
    )

    mood = models.CharField(
        choices=[(option['key'], option['key']) for option in constants.moods()],
        max_length=max([len(option['key']) for option in constants.moods()]),
        default=constants.MOOD_ANY['key'],
        null=False
    )

    admin = models.ForeignKey(
        to='users.User',
        related_name='rooms_as_admin',
        null=False,
        on_delete=models.deletion.CASCADE
    )

    users = models.ManyToManyField(
        to='users.User',
        related_name='rooms'
    )

    movies = models.ManyToManyField(
        to='movies.Movie',
        related_name='rooms'
    )

    results = models.ManyToManyField(
        to='movies.Movie',
        related_name='rooms_as_results'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def sync_user(self, user) -> None:
        self.users.add(user)

    @property
    def users_are_ready(self) -> bool:
        total_expected_ratings = self.users.count() * constants.CHALLENGE_MOVIES
        total_ratings = sum([user['rated_count'] for user in self.users.rated_count(self)])
        return total_expected_ratings == total_ratings

    def get_or_create_results(self):
        if self.results.exists():
            return self.results.all()

        # lets get them if we can!

        if not self.users_are_ready:
            raise RoomUsersNotReady

        results = get_proxy().get_recommendation(constants.RESULTS_MOVIES)
        if len(results) != constants.RESULTS_MOVIES:
            raise IntegrityError
        self.results.set(results)

        return self.results



