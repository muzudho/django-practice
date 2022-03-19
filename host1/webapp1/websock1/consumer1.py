# See also:
#     📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
#     📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class Websock1Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected")
        self.room_name = 'room_1'
        self.room_group_name = 'room_group_1'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        """
        print("Received")
        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'message': text_data,
        })

    async def send_message(self, res):
        """ Receive message from room group """
        print("Sent message")
        # Send message to WebSocket
        await self.send(text_data=res)
