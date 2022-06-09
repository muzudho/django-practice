# 参考にした記事
# -------------
# 📖[Django Channels and WebSockets](https: // blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from webapp1.websocks.tic_tac_toe.v2.protocol import TicTacToeV2Protocol
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV2ConsumerBase(AsyncJsonWebsocketConsumer):
    #           ^

    def __init__(self):
        super().__init__()
        self._protocol = TicTacToeV2Protocol()

    async def connect(self):
        """接続"""
        print("Connect")
        # print(f"Connect self.scope={self.scope}")
        # print(
        #     f'Connect self.scope["cookies"]["csrftoken"]={self.scope["cookies"]["csrftoken"]}')
        # print(f'Connect self.scope["session"]={self.scope["session"]}')
        # print(f'Connect self.scope["user"]={self.scope["user"]}')

        # ログインしていれば、ユーザーのPrimaryKeyは以下で取得可能。ログインしていなければ None
        print(
            f'Connect self.scope["user"].pk={self.scope["user"].pk}')
        # print(
        #    f'Connect self.scope["user"].username={self.scope["user"].username}')

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

        # ログインしていなければ AnonymousUser
        user = self.scope["user"]
        print(f"[TicTacToeV2ConsumerCustom on_receive] user=[{user}]")
        response = await self._protocol.execute(doc_received, user)

        # 部屋のメンバーに一斉送信します
        await self.channel_layer.group_send(self.room_group_name, response)

    async def send_message(self, message):
        """メッセージ送信"""
        await self.send(text_data=json.dumps({
            "message": message,
        }))
