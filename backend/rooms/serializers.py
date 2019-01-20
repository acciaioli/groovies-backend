from rest_framework import serializers

from users.models import User
from .models import Room


class UserInRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)
        read_only_fields = ('name',)


class RoomSerializer(serializers.ModelSerializer):
    users = UserInRoomSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data['admin'] = self.context['request'].user
        room = super().create(validated_data)
        room.initialize_users()
        return room

    class Meta:
        model = Room
        fields = ('slug', 'mood', 'admin', 'users')
        read_only_fields = ('admin', )
