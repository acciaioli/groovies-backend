from typing import List
from abc import ABC, abstractmethod

from movies.models import Movie


class MLProxyInterface(ABC):
    @staticmethod
    @abstractmethod
    def get_challenge() -> List[Movie]:
        pass

    @staticmethod
    @abstractmethod
    def get_recommendation() -> List[Movie]:
        pass
