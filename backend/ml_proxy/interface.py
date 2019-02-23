from typing import List
from abc import ABC, abstractmethod

from movies.models import Movie


class MLProxyInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_challenge(n: int) -> List[Movie]:
        pass  # pragma: no cover

    @staticmethod
    @abstractmethod
    def get_recommendation(n: int) -> List[Movie]:
        pass  # pragma: no cover
