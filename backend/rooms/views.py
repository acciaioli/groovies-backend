from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from movies.serializers import MovieSerializer
from .exceptions import RoomUsersNotReady
from .models import Room
from .serializers import RoomSerializer
from .permissions import RoomPermissions


class RoomViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    model_class = Room
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated, RoomPermissions)

    lookup_field = 'slug'

    queryset = model_class.objects.all()

    @action(detail=True, methods=['patch'], permission_classes=(IsAuthenticated,))
    def join(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def results(self, request, *args, **kwargs):
        room = self.get_object()
        try:
            results = room.get_or_create_results()
        except RoomUsersNotReady:
            raise ValidationError('room users are not ready for results')

        return Response(MovieSerializer(results, many=True).data)
