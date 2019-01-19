from rest_framework import mixins
from rest_framework import viewsets

from .models import User
from .serializers import SessionUserSerializer
from .permissions import UserPermissions


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model_class = User
    serializer_class = SessionUserSerializer
    permission_classes = (UserPermissions,)

    lookup_field = 'username'

    queryset = model_class.objects.all()
