from typing import Dict, List, Optional

from rest_framework import serializers

from users.models import User
from movies.serializers import MovieSerializer
from .exceptions import RoomUsersNotReady
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField(read_only=True)
    movies = MovieSerializer(many=True, read_only=True)
    unrated_movies = serializers.SerializerMethodField(read_only=True)

    @property
    def user(self) -> Optional[User]:
        try:
            return self.context['request'].user
        except KeyError:
            return None

    def get_users(self, room: Room) -> List[Dict]:
        return list(room.users.rated_count(room))

    def get_unrated_movies(self, room: Room) -> List[Dict]:
        qs = room.movies.unrated(user=self.user)
        return MovieSerializer(qs, many=True).data

    def update(self, instance, validated_data):
        instance.sync_user(self.context['request'].user)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        return self.Meta.model.objects.create_room(admin=self.context['request'].user, **validated_data)

    class Meta:
        model = Room
        fields = ('slug', 'mood', 'admin', 'users', 'movies', 'unrated_movies')
        read_only_fields = ('admin', )


class RoomResultsSerializer(serializers.ModelSerializer):
    results = serializers.SerializerMethodField(read_only=True)

    def get_results(self, room):
        try:
            qs = room.get_or_create_results()
        except RoomUsersNotReady:
            raise serializers.ValidationError('room users are not ready for results')

        return MovieSerializer(qs, many=True).data

    class Meta:
        model = Room
        fields = ('slug', 'results')
        read_only_fields = ('slug',)
