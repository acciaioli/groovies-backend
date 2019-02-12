from typing import Any, Callable

from cachedprop import cpd
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Room


class RoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cpd
    def user(self):
        return self.scope['user']

    @property
    def room(self) -> Room:
        qs_kwargs = self.scope['url_route']['kwargs']
        return Room.objects.get(**qs_kwargs)

    def connect(self):
        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            'ola',  # self.room.slug,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            'ola',  # self.room.slug,
            {
                'type': 'chat_message',
                'message': 'channellllllss'
            }
        )

        self.send_json({'hello': 'sockets'})

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send_json({'message': message})

    def disconnect(self, close_code):
        pass

    def receive_json(self, content, **kwargs):
        async_to_sync(self.channel_layer.group_send)(
            self.room.slug,
            {
                'type': 'chat_message',
                'message': 'mirror'
            }
        )


