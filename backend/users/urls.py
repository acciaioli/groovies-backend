from rest_framework import routers
from .views import UserViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet, 'users')

urlpatterns = router.urls
