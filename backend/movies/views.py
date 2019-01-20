from rest_framework import viewsets


from .models import Movie
from .serializers import MovieSerializer
from .permissions import MoviesPermissions


class MoviesViewSet(viewsets.GenericViewSet):
    model_class = Movie
    serializer_class = MovieSerializer
    permission_classes = (MoviesPermissions,)

    queryset = model_class.objects.all()
