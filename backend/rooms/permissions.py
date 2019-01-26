from rest_framework.permissions import BasePermission


class RoomPermissions(BasePermission):
    def has_object_permission(self, request, view, room):
        return room.users.filter(pk=request.user.pk).exists()
