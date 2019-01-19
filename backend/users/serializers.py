from rest_framework import serializers

from .models import User


class SessionUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_session_user(validated_data['name'])

    class Meta:
        model = User
        fields = ('name', )
