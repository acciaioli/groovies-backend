import json

from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase

from users.models import User
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

    def test_initialize_users(self):
        room = Room.objects.create(slug=self.slug, admin=self.user)
        self.assertEqual(list(room.users.all()), [])
        room.initialize_users()
        self.assertEqual(list(room.users.all()), [self.user])


class TestRoomManager(TestCase):
    def setUp(self):
        self.slug = 'iceland'
        self.user = User.objects.create_user(**USER_JOAO)

    def test_create_room_success(self):
        room = Room.objects.create_room(**{'slug': self.slug, 'admin': self.user})
        self.assertEqual(room.slug, self.slug)
        self.assertEqual(list(room.users.all()), [self.user])


class TestRoomsApi(APITestCase):
    URL = '/rooms'
    CONTENT_TYPE = 'application/json'

    def setUp(self):
        self.user = User.objects.create_user(**USER_JOAO)

        self.http_auth = {'HTTP_AUTHORIZATION': f'JWT {self.user.create_jwt()}'}

        self.room = Room.objects.create_room(slug='porchester', admin=User.objects.create_user(**USER_CHI))

    def test_create_401(self):
        self.assertEqual(Room.objects.count(), 1)
        post_data = {'slug': 'iceland'}
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Room.objects.count(), 1)

    def test_create_201(self):
        self.assertEqual(Room.objects.count(), 1)
        post_data = {'slug': 'iceland'}
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Room.objects.count(), 2)
        self.assertEqual(len(response.json()), 4)
        self.assertEqual(response.json()['slug'], 'iceland')
        self.assertEqual(response.json()['mood'], constants.MOOD_ANY['key'])
        self.assertEqual(response.json()['admin'], self.user.pk)
        self.assertEqual(response.json()['users'], [{'name': self.user.name}])

    def test_join_401(self):
        self.assertEqual(Room.objects.count(), 1)
        url = f'{self.URL}/{self.room.slug}/join'
        response = self.client.put(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Room.objects.count(), 1)

    def test_join_200(self):
        self.assertEqual(Room.objects.count(), 1)
        self.assertEqual(self.room.users.count(), 1)
        url = f'{self.URL}/{self.room.slug}/join'
        response = self.client.put(url, **self.http_auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Room.objects.count(), 1)
        self.room.refresh_from_db()
        self.assertEqual(self.room.users.count(), 2)
        self.assertIn({'name': self.user.name}, list(self.room.users.all()))

