from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase

from users.models import User
from ratings.models import Rating
from .models import Movie


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


class TestMovieModel(TestCase):
    def setUp(self):
        self.title = 'The Prestige'
        self.year = "2006"

    def test_create_no_title_fail(self):
        with self.assertRaises(IntegrityError):
            Movie.objects.create(year=self.year)

    def test_create_no_year_fail(self):
        with self.assertRaises(IntegrityError):
            Movie.objects.create(title=self.title)

    def test_create_success(self):
        Movie.objects.create(title=self.title, year=self.year)


class TestMovieManager(TestCase):
    def setUp(self):
        self.n = 10
        [Movie.objects.create(title=f'title_{i}', year=2019) for i in range(self.n)]

        self.user_1 = User.objects.create_user(**USER_JOAO)
        self.user_2 = User.objects.create_user(**USER_CHI)

    def test_unrated(self):
        qs = Movie.objects.order_by('?')
        rated_0 = qs[0]
        rated_1 = qs[1]
        rated_2 = qs[2]
        Rating.objects.create(user=self.user_1, movie=rated_0, score=1)
        Rating.objects.create(user=self.user_1, movie=rated_1, score=2)
        Rating.objects.create(user=self.user_2, movie=rated_2, score=3)

        unrated_1 = Movie.objects.unrated(user=self.user_1)
        unrated_2 = Movie.objects.unrated(user=self.user_2)

        self.assertEqual(unrated_1.count(), self.n - 2)
        self.assertNotIn(rated_0, unrated_1)
        self.assertNotIn(rated_1, unrated_1)

        self.assertEqual(unrated_2.count(), self.n - 1)
        self.assertNotIn(rated_2, unrated_2)


class TestMovieSerializer(TestCase):
    pass


class TestMoviesApi(APITestCase):
    URL = '/movies'
    CONTENT_TYPE = 'application/json'
