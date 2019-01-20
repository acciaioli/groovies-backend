from rest_framework import serializers

from users.models import User
from movies.serializers import MovieSerializer
from .models import Room


class UserInRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name',)
        read_only_fields = ('name',)


class RoomSerializer(serializers.ModelSerializer):
    users = UserInRoomSerializer(many=True, read_only=True)
    movies = MovieSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.sync_user(self.context['request'].user)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return self.Meta.model.objects.create_room(admin=self.context['request'].user, **validated_data)

    class Meta:
        model = Room
        fields = ('slug', 'mood', 'admin', 'users', 'movies')
        read_only_fields = ('admin', )
