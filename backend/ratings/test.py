import json

from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase

from users.models import User
from movies.models import Movie
from .models import Rating


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

MOVIE = {
    'title': 'The Prestige',
    'year': "2006"
}


class TestRatingModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(**USER_JOAO)
        self.movie = Movie.objects.create(**MOVIE)

    def test_create_no_user_fail(self):
        with self.assertRaises(IntegrityError):
            Rating.objects.create(movie=self.movie)

    def test_create_no_movie_fail(self):
        with self.assertRaises(IntegrityError):
            Rating.objects.create(user=self.user)

    def test_create_success(self):
        Rating.objects.create(user=self.user, movie=self.movie)


class TestRatingManager(TestCase):
    pass


class TestRatingSerializer(TestCase):
    pass


class TestRatingsApi(APITestCase):
    URL = '/ratings'
    CONTENT_TYPE = 'application/json'

    def setUp(self):
        self.user = User.objects.create_user(**USER_JOAO)
        self.movie = Movie.objects.create(**MOVIE)

        self.http_auth = {'HTTP_AUTHORIZATION': f'JWT {self.user.create_jwt()}'}

    def test_create_401(self):
        self.assertEqual(Rating.objects.count(), 0)
        post_data = {'movie': self.movie.id, 'score': 5}
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Rating.objects.count(), 0)

    def test_create_400(self):
        self.assertEqual(Rating.objects.count(), 0)
        post_data = {'movie': self.movie.id}
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'score': ['This field is required.']})
        self.assertEqual(Rating.objects.count(), 0)

        post_data['score'] = 6  # > 5
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'score': ['Ensure this value is less than or equal to 5.']})
        self.assertEqual(Rating.objects.count(), 0)

        post_data['score'] = 0  # < 1
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'score': ['Ensure this value is greater than or equal to 1.']})
        self.assertEqual(Rating.objects.count(), 0)

    def test_create_201(self):
        self.assertEqual(Rating.objects.count(), 0)
        post_data = {
            'movie': self.movie.id,
            'score': 5
        }
        response = self.client.post(self.URL, data=json.dumps(post_data), content_type=self.CONTENT_TYPE, **self.http_auth)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()['user'], self.user.pk)
        self.assertEqual(response.json()['movie'], self.movie.pk)
        self.assertEqual(response.json()['score'], 5)

        self.assertEqual(Rating.objects.count(), 1)
        rating = Rating.objects.first()
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.movie, self.movie)
        self.assertEqual(rating.score, 5)
        self.assertEqual(Rating.objects.count(), 1)
