from rest_framework import serializers

from .models import User


class SessionUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj: User):
        return obj.create_jwt()

    def create(self, validated_data):
        return User.objects.create_session_user(validated_data['name'])

    class Meta:
        model = User
        fields = ('name', 'token')
