from rest_framework import routers

from .views import MoviesViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'movies', MoviesViewSet, 'movies')

urlpatterns = router.urls
