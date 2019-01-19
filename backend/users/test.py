import json
from typing import Optional
from unittest.mock import patch

from django.contrib.auth import authenticate
from django.core import mail
from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings
from jwt import ExpiredSignature, DecodeError

from .models import User
# from .serializers import ConfirmEmailSerializer
# from .tasks import broadcast_registration, send_confirmation_email, on_create


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


class TestUserModel(TestCase):
    def test_create_jwt(self):
        user = User.objects.create_user(**USER_CHI)
        token = user.create_jwt()
        try:
            api_settings.JWT_DECODE_HANDLER(token)
        except (ExpiredSignature, DecodeError):
            self.assertTrue(False)
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

    def test_create_user_200(self):
        self.assertEqual(User.objects.count(), 0)
        post_data = {
            'name': USER_JOAO['name']
        }

        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()), 2)
        self.assertIn(response.json(), 'user')
        self.assertIn(response.json(), 'token')

        user_joao = User.objects.get(username=USER_JOAO['username'])
        self.assertEqual(user_joao.username, USER_JOAO['username'])
