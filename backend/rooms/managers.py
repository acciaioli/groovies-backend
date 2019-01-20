from django.db import models, IntegrityError

from ml_proxy import get_proxy
from users.models import User


class RoomManager(models.Manager):
    CHALLENGE_MOVIES = 10

    use_in_migrations = True

    def create_room(self, admin: User, **kwargs):
        movies = get_proxy().get_challenge()
        if len(movies) < self.CHALLENGE_MOVIES:
            raise IntegrityError
        room = self.create(admin=admin, **kwargs)
        room.movies.set(movies)
        room.sync_user(room.admin)
        return room
