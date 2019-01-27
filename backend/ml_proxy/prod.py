from typing import List

from movies.models import Movie
from .interface import MLProxyInterface


class ProductionMLProxy(MLProxyInterface):
    """
    This is the only class in our app that will be aware of the ML service interface
    """

    @staticmethod
    def get_challenge(n: int) -> List[Movie]:
        return []

    @staticmethod
    def get_recommendation(n: int) -> List[Movie]:
        return []
