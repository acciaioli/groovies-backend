from rest_framework import routers

from .views import RatingsViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'ratings', RatingsViewSet, 'ratings')

urlpatterns = router.urls
