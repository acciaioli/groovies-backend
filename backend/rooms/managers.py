from django.db import models, IntegrityError

from ml_proxy import get_proxy
from users.models import User
from .constants import CHALLENGE_MOVIES


class RoomManager(models.Manager):
    def create_room(self, admin: User, **kwargs):
        movies = get_proxy().get_challenge(n=CHALLENGE_MOVIES)
        if len(movies) != CHALLENGE_MOVIES:
            raise IntegrityError
        room = self.create(admin=admin, **kwargs)
        room.movies.set(movies)
        room.sync_user(room.admin)
        return room
