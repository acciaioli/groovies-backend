from django.conf.urls import url
from rest_framework import routers

from .views import RoomViewSet
from .consumers import RoomConsumer


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, 'rooms')

urlpatterns = router.urls


websocket_urlpatterns = [
    url(r'^ws/rooms/(?P<slug>[^/]+)/$', RoomConsumer),
]
