import os
import datetime

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


class StatusView(APIView):
    http_method_names = ['get']
    permission_classes = (AllowAny,)

    @staticmethod
    def __calculate_up_time():
        delta = datetime.datetime.now() - settings.START_DATETIME
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    def get(self, request, *args, **kwargs):
        return Response(
            status=status.HTTP_200_OK,
            data={
                'image': 'backend',
                'tag': os.getenv('DOCKER_IMAGE_TAG', 'dev'),
                'up_time': self.__calculate_up_time()
            },
            content_type='application/json')


status_view = StatusView.as_view()
