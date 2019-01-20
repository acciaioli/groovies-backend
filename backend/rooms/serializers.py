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

    def update(self, instance, validated_data):
        instance.sync_user(self.context['request'].user)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        validated_data['admin'] = self.context['request'].user
        instance = super().create(validated_data)

        instance.sync_user(self.context['request'].user)
        return instance

    class Meta:
        model = Room
        fields = ('slug', 'mood', 'admin', 'users')
        read_only_fields = ('admin', )
