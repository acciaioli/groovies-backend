import json

from django.contrib.auth import authenticate
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from jwt import ExpiredSignature, DecodeError

from movies.models import Movie
from ratings.models import Rating
from rooms.models import Room
from .models import User

USER_CHI = {
    'email': 'chi@groovies.com',
    'password': 'verystrong1',
    'name': 'Maria Chi'
}

USER_JOAO = {
    'email': 'joao@groovies.com',
    'password': 'verystrong2',
    'name': 'Jon Green'
}


class TestUserBackend(TestCase):
    def setUp(self):
        User.objects.create_user(**USER_CHI)
        User.objects.create_user(**USER_JOAO)

    def test_none_fail(self):
        self.assertIsNone(authenticate())

    def test_no_user_fail(self):
        self.assertIsNone(authenticate(email='bad_username'))

    def test_email_authentication_fail(self):
        self.assertIsNone(authenticate(email=USER_CHI['email'], password=USER_JOAO['password']))

    def test_email_authentication_success(self):
        self.assertIsNotNone(authenticate(email=USER_CHI['email'], password=USER_CHI['password']))


class TestUserManager(TestCase):
    def test_create_user_success(self):
        self.assertEqual(User.objects.count(), 0)
        user = User.objects.create_user(**USER_JOAO)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, USER_JOAO['email'])
        self.assertTrue(user.check_password(USER_JOAO['password']))
        self.assertEqual(user.name, USER_JOAO['name'])

    def test_create_user_success_no_name(self):
        self.assertEqual(User.objects.count(), 0)
        chi = dict(USER_CHI)
        chi.pop('name')
        user = User.objects.create_user(**chi)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, chi['email'])
        self.assertTrue(user.check_password(chi['password']))
        self.assertEqual(user.name, '')

    def test_create_session_user_success(self):
        self.assertEqual(User.objects.count(), 0)
        chi = dict(USER_CHI)
        chi.pop('name')
        user = User.objects.create_session_user(USER_CHI['name'])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.name, USER_CHI['name'])

    def test_room_ratings_count(self):
        movies_2018 = [Movie.objects.create(title=f'title_{i}', year=2018) for i in
                       range(Room.objects.CHALLENGE_MOVIES)]
        movies_2019 = [Movie.objects.create(title=f'title_{i}', year=2019) for i in
                       range(Room.objects.CHALLENGE_MOVIES)]
        user_1 = User.objects.create_session_user(USER_CHI['name'])
        user_2 = User.objects.create_session_user(USER_JOAO['name'])
        room = Room.objects.create(admin=user_1, slug='slug')
        room.sync_user(user_1)
        room.sync_user(user_2)
        room.movies.set(movies_2018)
        self.assertEqual(room.users.count(), 2)
        self.assertEqual(room.movies.count(), Room.objects.CHALLENGE_MOVIES)

        # 2018 movies ratings
        ratings = [
            Rating(user=user_1, movie=movies_2018[0], score=1),
            Rating(user=user_1, movie=movies_2018[3], score=2),
            Rating(user=user_1, movie=movies_2018[8], score=3),

            # 2019 movie ratings
            Rating(user=user_1, movie=movies_2019[1], score=1),
            Rating(user=user_1, movie=movies_2019[7], score=3),

            # user 2
            Rating(user=user_2, movie=movies_2019[0], score=1),
        ]
        Rating.objects.bulk_create(ratings)

        qs = User.objects.rated_count(room=room)
        self.assertEqual(qs.count(), 2)
        self.assertIn({
            'name': USER_CHI['name'],
            'rated_count': 3
        }, qs)
        self.assertIn({
            'name': USER_JOAO['name'],
            'rated_count': 0
        }, qs)


class TestUserModel(TestCase):
    def test_create_jwt(self):
        user = User.objects.create_user(**USER_CHI)
        token = user.create_jwt()
        try:
            api_settings.JWT_DECODE_HANDLER(token)
        # on success, the lines bellow will not run
        except (ExpiredSignature, DecodeError):  # pragma: no cover
            self.assertTrue(False)  # pragma: no cover
        bad_token = f'{token}_taint'
        with self.assertRaises(DecodeError):
            api_settings.JWT_DECODE_HANDLER(bad_token)


class TestUsersApi(APITestCase):
    """
    For the MVP we just want to be able to create users
    There will not be proper authentication.
    We will be creating new users every session
    """
    URL = '/users'
    CONTENT_TYPE = 'application/json'

    def test_create_user_201(self):
        self.assertEqual(User.objects.count(), 0)
        post_data = {'name': USER_JOAO['name']}
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()), 2)
        self.assertIn('name', response.json())
        self.assertIn('token', response.json(), )

        self.assertEqual(User.objects.count(), 1)
        user_joao = User.objects.first()
        self.assertEqual(user_joao.name, USER_JOAO['name'])
