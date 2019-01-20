from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase

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
    pass


class TestMovieSerializer(TestCase):
    pass


class TestMoviesApi(APITestCase):
    URL = '/movies'
    CONTENT_TYPE = 'application/json'
