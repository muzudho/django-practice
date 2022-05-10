# 参考にした記事
# -------------
# 📖[Django Channels and WebSockets](https: // blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from webapp1.tic_tac_toe2.protocol import Protocol


class TicTacToe3Consumer1(AsyncJsonWebsocketConsumer):
    #          ^

    def __init__(self):
        super().__init__()
        self.protocol = Protocol()

    async def connect(self):
        """接続"""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'  # 部屋名で集めるグループ
        print(f"Connect {self.room_name} {self.room_group_name}")

        # TODO 部屋を立てる？ 部屋数の上限は？ 立っている部屋を一覧できるか？

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """切断"""
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """クライアントからのメッセージの受信"""

        print(
            f"[Debug] Consumer1#receive text_data={text_data}")  # ちゃんと動いているようなら消す

        request = json.loads(text_data)
        response = self.protocol.execute(request)

        # 部屋のメンバーに一斉送信します
        await self.channel_layer.group_send(self.room_group_name, response)

    async def send_message(self, message):
        """メッセージ送信"""
        await self.send(text_data=json.dumps({
            "message": message,
        }))
