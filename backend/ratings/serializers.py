from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(allow_null=False, min_value=1, max_value=5)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = Rating
        fields = ('user', 'movie', 'score')
        read_only_fields = ('user', )
