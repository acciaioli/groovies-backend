from typing import List

from movies.models import Movie
from .interface import MLProxyInterface


class DevMLProxy(MLProxyInterface):
    """
    Here we will be "mocking" the the ProductionMLProxy
    so we don't depend on the MLService in development
    """

    @staticmethod
    def get_challenge() -> List[Movie]:
        return Movie.objects.all()[:10]

    @staticmethod
    def get_recommendation() -> List[Movie]:
        return Movie.objects.all()[10:15]
