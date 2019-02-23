from typing import Any, Dict, List
from abc import ABC, abstractmethod
from urllib import parse

from django.db import close_old_connections
from channels.routing import ProtocolTypeRouter, URLRouter
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from rooms.urls import websocket_urlpatterns


#############################################################################
class ChannelsMiddleware(ABC):
    def __init__(self, inner):
        self.inner = inner
        self.scope = {}

    @property
    def query_params(self) -> Dict[str, List[Any]]:
        query_str: str = self.scope['query_string'].decode('utf-8')
        return parse.parse_qs(query_str)

    def __call__(self, scope):
        self.scope = scope
        close_old_connections()
        self.intercept()
        return self.inner(self.scope)

    @abstractmethod
    def intercept(self) -> None:
        pass


class JWTAuthMiddleware(ChannelsMiddleware):

    def token(self) -> str:
        return self.query_params['JWT'][0]

    def intercept(self):
        serializer = VerifyJSONWebTokenSerializer(data={'token': self.token})
        if serializer.is_valid(raise_exception=False):
            user = serializer.validated_data['user']
        else:
            user = None
        self.scope['user'] = user
#############################################################################


application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
})
