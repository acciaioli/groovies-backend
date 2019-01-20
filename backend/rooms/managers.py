from django.db import models

from users.models import User


class RoomManager(models.Manager):
    use_in_migrations = True

    def create_room(self, admin: User, **kwargs):
        room = self.create(admin=admin, **kwargs)
        room.initialize_users()
        return room
