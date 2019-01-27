from typing import List

from movies.models import Movie
from .interface import MLProxyInterface


class DevMLProxy(MLProxyInterface):
    """
    Here we will be "mocking" the the ProductionMLProxy
    so we don't depend on the MLService in development
    """

    @staticmethod
    def get_challenge(n: int) -> List[Movie]:
        # return the n first movies
        return list(Movie.objects.all())[:n]

    @staticmethod
    def get_recommendation(n: int) -> List[Movie]:
        # return the n last movies
        return list(Movie.objects.all())[-n:]
