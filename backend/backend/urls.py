from django.urls import path, include

from backend.views import status_view

urlpatterns = [
    path('', status_view),
    path('', include('users.urls')),
    path('', include('rooms.urls'))
]
