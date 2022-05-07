# See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from webapp1.tic_tac_toe2.protocol import Protocol


class TicTacToe2Consumer1(AsyncJsonWebsocketConsumer):
    #          ^

    def __init__(self):
        super().__init__()
        self.protocol = Protocol()

    async def connect(self):
        print("Connect")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

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
        Get the event and send the appropriate event
        """
        print(
            f"[Debug] Consumer1#receive text_data={text_data}")  # ちゃんと動いているようなら消す
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)

        response = self.protocol.execute(event, message)

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, response)

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
