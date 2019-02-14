from typing import Any, Optional
from abc import ABC, abstractmethod

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from users.models import User
from .models import Room


#############################################################################
class BasePermission(ABC):
    @abstractmethod
    async def has_permission(self, consumer) -> bool:
        pass


class IsAuthenticated(BasePermission):
    async def has_permission(self, consumer: Any) -> bool:
        user = consumer.scope.get('user', None)
        return bool(user is not None and user.is_authenticated)
#############################################################################


class RoomConsumer(AsyncJsonWebsocketConsumer):
    sanity_classes = ()
    permission_classes = (IsAuthenticated,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = self._get_room()

    def _get_room(self) -> Optional[Room]:
        qs_kwargs = self.scope['url_route']['kwargs']
        return Room.objects.get(**qs_kwargs)

    @property
    def group_id(self) -> str:
        return self.room.slug

    @property
    def user(self) -> Optional[User]:
        return self.scope['user']

    def user_ratings_count(self):
        return self.room.users.rated_count(self.room)

    async def connect(self):
        for permission_class in self.permission_classes:
            if not await permission_class().has_permission(self):
                await self.close(code=401)
                return

        await self.accept()

        # Join room group
        await self.channel_layer.group_add(group=self.room.slug, channel=self.channel_name)

        await self.channel_layer.group_send(
            group=self.room.slug,
            message={'type': 'user.join'}
        )

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content, **kwargs):
        if 'type' not in content:
            return

        if content['type'] == 'user.update':
            await self.channel_layer.group_send(
                group=self.room.slug,
                message={'type': 'user.update'}
            )

    async def user_join(self, event):
        return await self.user_update(event)

    async def user_update(self, event):
        users = await database_sync_to_async(self.user_ratings_count)()
        await self.send_json(content=dict(event, users=list(users)))

#    def users_are_ready(self):
#        return self.room.users_are_ready
#
#    def room_get_or_create_results(self):
#        return self.room.get_or_create_results()
#
#    async def results_update(self):
#        results = await database_sync_to_async(self.room_get_or_create_results)()
#        await self.send_json(list(results))
#
#