# 参考にした記事
# -------------
# 📖[Django Channels and WebSockets](https: // blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TicTacToeV2ConsumerBase(AsyncJsonWebsocketConsumer):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()

    async def connect(self):
        """接続"""
        print("Connect")
        # ログインしていれば、ユーザーのPrimaryKeyは以下で取得可能。ログインしていなければ None
        # print(f'Connect self.scope["user"].pk={self.scope["user"].pk}')

        self.room_name = self.scope['url_route']['kwargs']['kw_room_name']
        self.room_group_name = f'room_{self.room_name}'

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

        doc_received = json.loads(text_data)

        response = self.on_receive(doc_received)

        # 部屋のメンバーに一斉送信します
        await self.channel_layer.group_send(self.room_group_name, response)

    def on_receive(self, doc_received):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """
        return {}  # Empty

    async def send_message(self, message):
        """メッセージ送信"""
        await self.send(text_data=json.dumps({
            "message": message,
        }))
