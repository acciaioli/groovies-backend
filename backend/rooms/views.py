from rest_framework import mixins
from rest_framework import viewsets

from .models import Room
from .serializers import RoomSerializer
from .permissions import RoomPermissions


class RoomViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model_class = Room
    serializer_class = RoomSerializer
    permission_classes = (RoomPermissions,)

    lookup_field = 'slug'

    queryset = model_class.objects.all()
