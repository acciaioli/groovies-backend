from rest_framework import routers

from .views import RoomViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'rooms', RoomViewSet, 'rooms')

urlpatterns = router.urls
