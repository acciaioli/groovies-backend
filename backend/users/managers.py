import uuid

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

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
