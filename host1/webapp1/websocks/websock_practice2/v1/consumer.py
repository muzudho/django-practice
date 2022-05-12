# See also:
#     📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
#     📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
#     📖 [Channels - Channel Layers](https://channels.readthedocs.io/en/stable/topics/channel_layers.html)
from channels.generic.websocket import AsyncJsonWebsocketConsumer
#                                           ----
#                                           1
# 1. Json を使うものに変更


class WebsockPractice2V1Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """Called when the websocket is handshaking as part of initial connection."""
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        """Called when the WebSocket closes for any reason."""
        print("Disconnected")

    async def receive_json(self, doc):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        print("Received JSON")
        # Send message to WebSocket
        await self.send(text_data=f"Echo: {doc}")

    async def send_message(self, res):
        """ Receive message from room group """
        print("Sent message")
        # Send message to WebSocket
        await self.send(text_data=res)
