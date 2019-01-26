import uuid

from django.db.models import Count, Q
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        email_ = kwargs['email']
        name = kwargs.get('name', '')
        password = kwargs['password']
        email = self.normalize_email(email_)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_session_user(self, name: str):
        email = f'{uuid.uuid4().hex}@groovies.com'
        password = f'pw_{uuid.uuid4().hex}'

        return self.create_user(email=email, password=password, name=name)

    def rated_count(self, room):
        users = list(room.users.values_list('pk', flat=True))
        movies = list(room.movies.values_list('pk', flat=True))
        rated_count = Count('ratings', filter=Q(ratings__movie__in=movies))
        return super().get_queryset().values('name').filter(pk__in=users).annotate(rated_count=rated_count)
