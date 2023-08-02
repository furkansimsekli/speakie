import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    async def connect(self):
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()

        await self.channel_layer.group_add(f'user_{self.user.id}', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f'user_{self.user.id}', self.channel_name)

    async def notify_user(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
