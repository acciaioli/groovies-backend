from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    def get_score(self, o):
        return 0

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'description', 'url', 'score')
        read_only_fields = ('title', 'year', 'description', 'url')
