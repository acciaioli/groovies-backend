from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets

from .models import Rating
from .serializers import RatingSerializer
from .permissions import RatingsPermissions


class RatingsViewSet(CreateModelMixin, viewsets.GenericViewSet):
    model_class = Rating
    serializer_class = RatingSerializer
    permission_classes = (RatingsPermissions,)

    queryset = model_class.objects.all()
