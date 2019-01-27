import json
from unittest.mock import patch

from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase

from users.models import User
from movies.models import Movie
from ratings.models import Rating
from .exceptions import RoomUsersNotReady
from .models import Room
from . import constants


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


class TestRoomModel(TestCase):
    def setUp(self):
        self.slug = 'iceland'
        self.user = User.objects.create_user(**USER_JOAO)

    def test_create_no_slug_fail(self):
        with self.assertRaises(IntegrityError):
            Room.objects.create(admin=self.user)

    def test_create_not_unique_slug_fail(self):
        Room.objects.create(slug=self.slug, admin=self.user)
        with self.assertRaises(IntegrityError):
            Room.objects.create(slug=self.slug, admin=self.user)

    def test_create_no_mood_fail(self):
        with self.assertRaises(IntegrityError):
            Room.objects.create(slug=self.slug, admin=self.user, mood=None)

    def test_create_no_admin_fail(self):
        with self.assertRaises(IntegrityError):
            Room.objects.create(slug=self.slug)

    def test_create_success(self):
        Room.objects.create(slug=self.slug, admin=self.user)

    def test_sync_users(self):
        room = Room.objects.create(slug=self.slug, admin=self.user)
        self.assertEqual(list(room.users.all()), [])
        room.sync_user(room.admin)
        room.refresh_from_db()
        self.assertEqual(list(room.users.all()), [self.user])


class TestRoomManager(TestCase):
    def setUp(self):
        self.slug = 'iceland'
        self.user = User.objects.create_user(**USER_JOAO)

        [Movie.objects.create(title=f'title_{i}', year=2019)
         for i in range(constants.CHALLENGE_MOVIES + constants.RESULTS_MOVIES)]

    def test_create_room_success(self):
        room = Room.objects.create_room(**{'slug': self.slug, 'admin': self.user})
        self.assertEqual(room.slug, self.slug)
        self.assertEqual(list(room.users.all()), [self.user])

    def test_create_room_fail_no_movies(self):
        Movie.objects.all().delete()
        self.assertTrue(constants.CHALLENGE_MOVIES > Movie.objects.count())
        # we dont have enough movies to create a room
        with self.assertRaises(IntegrityError):
            Room.objects.create_room(**{'slug': self.slug, 'admin': self.user})

    def test_create_room_success_movies(self):
        room = Room.objects.create_room(**{'slug': self.slug, 'admin': self.user})
        self.assertEqual(room.slug, self.slug)
        self.assertEqual(room.movies.count(), constants.CHALLENGE_MOVIES)

    def test_sync_user(self):
        room = Room.objects.create_room(**{'slug': self.slug, 'admin': self.user})
        user_2 = User.objects.create_user(**USER_CHI)
        self.assertNotEqual(list(room.users.all()), list(User.objects.all()))
        room.sync_user(user_2)
        self.assertEqual(list(room.users.all()), list(User.objects.all()))

    def test_get_or_create_results(self):
        room = Room.objects.create_room(**{'slug': self.slug, 'admin': self.user})
        self.assertEqual(list(room.results.all()), [])
        user_2 = User.objects.create_user(**USER_CHI)
        room.sync_user(user_2)
        admin_rated_count = room.users.rated_count(room)[0]['rated_count']
        user_2_rated_count = room.users.rated_count(room)[1]['rated_count']
        self.assertTrue(admin_rated_count < constants.CHALLENGE_MOVIES)
        self.assertTrue(user_2_rated_count < constants.CHALLENGE_MOVIES)

        self.assertEqual(room.users_are_ready, False)
        with self.assertRaises(RoomUsersNotReady):
            room.get_or_create_results()

        Rating.objects.bulk_create([Rating(user=self.user, movie=movie, score=1) for movie in list(room.movies.all())])
        admin_rated_count = room.users.rated_count(room)[0]['rated_count']
        self.assertEqual(admin_rated_count, constants.CHALLENGE_MOVIES)

        self.assertEqual(room.users_are_ready, False)
        with self.assertRaises(RoomUsersNotReady):
            room.get_or_create_results()

        Rating.objects.bulk_create([Rating(user=user_2, movie=movie, score=1) for movie in list(room.movies.all())])
        user_2_rated_count = room.users.rated_count(room)[1]['rated_count']
        self.assertEqual(user_2_rated_count, constants.CHALLENGE_MOVIES)

        self.assertEqual(room.users_are_ready, True)
        results = room.get_or_create_results()
        room.refresh_from_db()
        self.assertEqual(list(room.results.all()), list(results.all()))
        self.assertEqual(results.count(), constants.RESULTS_MOVIES)

        results_2 = room.get_or_create_results()
        self.assertEqual(list(results_2.all()), list(results.all()))


class TestRoomSerializer(TestCase):
    pass


class TestRoomsApi(APITestCase):
    URL = '/rooms'
    CT = 'application/json'

    def setUp(self):
        [Movie.objects.create(title=f'title_{i}', year=2019) for i in range(20)]

        self.user = User.objects.create_user(**USER_JOAO)
        self.admin = User.objects.create_user(**USER_CHI)
        self.http_auth = {'HTTP_AUTHORIZATION': f'JWT {self.user.create_jwt()}'}
        self.http_admin_auth = {'HTTP_AUTHORIZATION': f'JWT {self.admin.create_jwt()}'}

        self.room = Room.objects.create_room(slug='porchester', admin=self.admin)

    def test_create_401(self):
        self.assertEqual(Room.objects.count(), 1)
        post_data = json.dumps({'slug': 'iceland'})
        r = self.client.post(self.URL, data=post_data, content_type=self.CT)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(Room.objects.count(), 1)

    def test_create_201(self):
        self.assertEqual(Room.objects.count(), 1)
        post_data = json.dumps({'slug': 'iceland'})
        r = self.client.post(self.URL, data=post_data, content_type=self.CT, **self.http_auth)

        self.assertEqual(r.status_code, 201)
        r_json = r.json()
        self.assertEqual(len(r_json), 6)
        self.assertEqual(r_json['slug'], 'iceland')
        self.assertEqual(r_json['mood'], constants.MOOD_ANY['key'])
        self.assertEqual(r_json['admin'], self.user.pk)
        self.assertEqual(r_json['users'], [{'name': self.user.name, 'rated_count': 0}])
        self.assertEqual(len(r_json['movies']), constants.CHALLENGE_MOVIES)
        self.assertEqual(r_json['unrated_movies'], r_json['movies'])

        self.assertEqual(Room.objects.count(), 2)
        created_room = Room.objects.get(slug='iceland')
        self.assertEqual(created_room.mood, constants.MOOD_ANY['key'])
        self.assertEqual(created_room.admin, self.user)
        self.assertEqual(list(created_room.users.all()), [self.user])
        self.assertEqual(created_room.movies.count(), constants.CHALLENGE_MOVIES)

    def test_retrieve_401(self):
        url = f'{self.URL}/{self.room.slug}'
        r = self.client.get(url)
        self.assertEqual(r.status_code, 401)

    def test_retrieve_403(self):
        url = f'{self.URL}/{self.room.slug}'
        r = self.client.get(url, **self.http_auth)
        self.assertEqual(r.status_code, 403)

    def test_retrieve_200(self):
        self.assertEqual(Room.objects.count(), 1)
        url = f'{self.URL}/{self.room.slug}'

        r = self.client.get(url, **self.http_admin_auth)
        self.assertEqual(r.status_code, 200)
        r_json = r.json()
        self.assertEqual(len(r_json), 6)
        self.assertEqual(r_json['slug'], self.room.slug)
        self.assertEqual(r_json['mood'], self.room.mood)
        self.assertEqual(r_json['admin'], self.admin.pk)
        self.assertEqual(r_json['users'], [{'name': self.room.admin.name, 'rated_count': 0}])
        self.assertEqual(len(r_json['movies']), constants.CHALLENGE_MOVIES)
        self.assertEqual(r_json['unrated_movies'], r_json['movies'])

        rated_movie = self.room.movies.order_by('?').first()
        Rating.objects.create(user=self.admin, movie=rated_movie, score=3)
        r_2 = self.client.get(url, **self.http_admin_auth)
        r_2_json = r_2.json()
        self.assertEqual(r_2.status_code, 200)
        self.assertEqual(len(r_2_json), 6)
        self.assertEqual(r_2_json['slug'], r_json['slug'])
        self.assertEqual(r_2_json['mood'], r_json['mood'])
        self.assertEqual(r_2_json['admin'], r_json['admin'])
        self.assertEqual(r_2_json['users'], [{'name': self.room.admin.name, 'rated_count': 1}])
        self.assertEqual(
            len(r_2_json['movies']), len(r_json['movies']))
        self.assertEqual(
            len(r_2_json['unrated_movies']), len(r_json['unrated_movies']) - 1),

    def test_join_401(self):
        url = f'{self.URL}/{self.room.slug}/join'
        r = self.client.patch(url)
        self.assertEqual(r.status_code, 401)

    def test_join_200(self):
        self.assertEqual(self.room.users.count(), 1)
        self.assertEqual(self.room.movies.count(), constants.CHALLENGE_MOVIES)
        url = f'{self.URL}/{self.room.slug}/join'
        r = self.client.patch(url, **self.http_auth)

        self.assertEqual(r.status_code, 200)
        r_json = r.json()
        self.assertEqual(len(r_json), 6)
        self.assertEqual(r_json['slug'], self.room.slug)
        self.assertEqual(r_json['mood'], self.room.mood)
        self.assertEqual(r_json['admin'], self.room.admin.pk)
        self.assertEqual(len(r_json['users']), 2)
        self.assertEqual(len(r_json['movies']), constants.CHALLENGE_MOVIES)
        self.assertEqual(len(r_json['movies']), constants.CHALLENGE_MOVIES)
        self.assertEqual(r_json['unrated_movies'], r_json['movies'])

        self.assertEqual(Room.objects.count(), 1)
        self.room.refresh_from_db()
        self.assertEqual(self.room.users.count(), 2)
        self.assertEqual(list(self.room.users.all()), [self.user, self.room.admin])
        self.assertEqual(self.room.movies.count(), constants.CHALLENGE_MOVIES)

        # user can "join" again
        r_2 = self.client.patch(url, **self.http_auth)
        self.assertEqual(r_2.status_code, 200)
        r_2_json = r_2.json()
        self.assertEqual(len(r_2_json), 6)
        self.assertEqual(r_2_json['slug'], r_json['slug'])
        self.assertEqual(r_2_json['mood'], r_json['mood'])
        self.assertEqual(r_2_json['admin'], r_json['admin'])
        self.assertEqual(r_2_json['users'], r_json['users'])
        self.assertEqual(len(r_2_json['movies']), len(r_json['movies']))
        self.assertEqual(len(r_2_json['unrated_movies']), len(r_json['unrated_movies'])),

        self.assertEqual(Room.objects.count(), 1)
        self.room.refresh_from_db()
        self.assertEqual(self.room.users.count(), 2)
        self.assertEqual(list(self.room.users.all()), [self.user, self.room.admin])
        self.assertEqual(self.room.movies.count(), constants.CHALLENGE_MOVIES)

    def test_results_401(self):
        url = f'{self.URL}/{self.room.slug}/results'
        r = self.client.get(url)
        self.assertEqual(r.status_code, 401)

    def test_results_403(self):
        url = f'{self.URL}/{self.room.slug}/results'
        r = self.client.get(url, **self.http_auth)
        self.assertEqual(r.status_code, 403)

    def test_results_400(self):
        self.assertEqual(self.room.users.count(), 1)
        self.assertFalse(self.room.users_are_ready)

        url = f'{self.URL}/{self.room.slug}/results'
        r = self.client.get(url, **self.http_admin_auth)
        self.assertEqual(r.status_code, 400)

    def test_results_200(self):
        self.assertEqual(self.room.users.count(), 1)
        self.assertEqual(self.room.users.first(), self.admin)
        Rating.objects.bulk_create([Rating(user=self.admin, movie=movie, score=5)
                                    for movie in list(self.room.movies.all())])
        self.assertTrue(self.room.users_are_ready)
        self.assertEqual(self.room.results.count(), 0)

        url = f'{self.URL}/{self.room.slug}/results'
        r = self.client.get(url, **self.http_admin_auth)
        self.assertEqual(r.status_code, 200)
        r_json = r.json()
        self.assertEqual(len(r_json), constants.RESULTS_MOVIES)
        self.room.refresh_from_db()
        self.assertEqual(self.room.results.count(), constants.RESULTS_MOVIES)

        # can be called again
        r_2 = self.client.get(url, **self.http_admin_auth)
        self.assertEqual(r_2.status_code, 200)
        r_2_json = r_2.json()
        self.assertEqual(r_2_json, r_json)
