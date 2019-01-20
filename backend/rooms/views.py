from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework import response

from .models import Room
from .serializers import RoomSerializer
from .permissions import RoomPermissions


class RoomViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model_class = Room
    serializer_class = RoomSerializer
    permission_classes = (RoomPermissions,)

    lookup_field = 'slug'

    queryset = model_class.objects.all()

    @decorators.action(detail=True, methods=['patch'])
    def join(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
