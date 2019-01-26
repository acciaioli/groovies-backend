from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer
from .permissions import RoomPermissions


class RoomViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    model_class = Room
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated, RoomPermissions)

    lookup_field = 'slug'

    queryset = model_class.objects.all()

    @action(detail=True, methods=['patch'], permission_classes=(IsAuthenticated,))
    def join(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
