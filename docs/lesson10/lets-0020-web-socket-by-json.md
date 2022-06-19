# 目的

Webサーバーとクライアント間でテキストを双方向の非同期通信するのは前にやった。  
今回は送受信するデータが JSON形式 しかないと割り切ってみる  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key              | Value                                     |
| ---------------- | ----------------------------------------- |
| OS               | Windows10                                 |
| Container        | Docker                                    |
| Web framework    | Django                                    |
| Communication    | JSON                                      |
| Program Language | Python 3                                  |
| Others           | Web socket                                |
| Editor           | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    ├── 📂sockapp1
    │    │   ├── 📄client.py
    │    │   ├── 📄echo_server.py
    │    │   └── 📄main_finally.py
    │    └── 📂websockapp1
    │        ├── 📄main_finally.py
    │        └── 📄websock_client.py
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄vuetify-desserts.json
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂websock_practice1
        │   │       └── 📂v1
        │   │           └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── <いろいろ>
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 設定の編集 - asgi.py ファイル

無ければ以下のファイルを作成、あればマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
👉          └── 📄asgi.py
```

```py
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack               # 追加
from channels.routing import ProtocolTypeRouter, URLRouter  # 追加
import webapp1.routing1
#      ------- --------
#      1       2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
#                                                --------
#                                                1
# 1. 設定モジュール名 `host1/settings.py`
#                          --------
#    例えばレッスンの最初に webapp1 アプリケーションを作成した場合、
#    デフォルトでは webapp1 アプリケーション用の設定モジュール名 `webapp1.settings` を指定するようになるので、
#                                                            ------- --------
#                                                            1o1     1o2
#    1o1. アプリケーション フォルダー名
#    1o2. settings.py ファイルの拡張子抜き
#
#    複数のアプリケーションの設定ファイルを指定するよう、トップフォルダーの settings.py に変更する

# （削除） application = get_asgi_application()
# （追加）
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            webapp1.routing1.websocket_urlpatterns
        )
    ),
})
```

# Step 3. コマンド実行

Dockerコンテナを停止させてほしい  

```shell
docker-compose down
```

Dockerコンテナを起動してほしい  

```shell
# requirements.txt を編集したので ビルドし直します
docker-compose build

# settings.py を編集したのでマイグレーションし直します
docker-compose run --rm web python3 manage.py migrate

# 起動
docker-compose up
```

# Step 4. consumer2.py ファイルを作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂websocks
            │   ├── 📂websock_practice1     # 1
            │   └── 📂websock_practice2     # 2
            │       └── 📂v1
👉          │           └── 📄consumer.py
            └── 📄asgi.py
```

```py
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
```

# Step 5. routing1.py ファイルを作成

無ければ以下のファイルを作成、あればマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂websocks
            │   ├── 📂websock_practice1     # 1
            │   └── 📂websock_practice2     # 2
            │       └── 📂v1
            │           └── 📄consumer.py
            ├── 📄asgi.py
👉          └── 📄routing1.py
```

```py
# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url

# Websock練習２
from webapp1.websocks.websock_practice2.v1.consumer import WebsockPractice2V1Consumer
#                                     ^                                   ^
#    ------- ----------------------------- --------        --------------------------
#    1       2                             3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

websocket_urlpatterns = [

    # Websock練習２
    url(r'^websock-practice2/v1/$', WebsockPractice2V1Consumer.as_asgi()),
    #                      ^                       ^
    #     -----------------------   ------------------------------------
    #     1                                      2
    # 1. URLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする

]
```

# Step 6. ローカルPCにPythonのパッケージ websocket-client をインストール

Step 1 ～ 5. は サーバーサイドだった。  
Step 6. からは クライアントサイドを説明する。  

（もうしているかもしれないが）あなたのPCでコマンドを打鍵してほしい。  

```shell
pip install websocket-client
```

# Step 7. websock_client.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    ├── 📂host_local1
    │    └── 📂websockapp1
👉  │        ├── 📄client2.py        # ここに新規作成
    │        └── 📄<いろいろ>
    └── 📂host1
        └── 📂webapp1
            ├── 📂websocks
            │   ├── 📂websock_practice1     # 1
            │   └── 📂websock_practice2     # 2
            │       └── 📂v1
            │           └── 📄consumer.py
            ├── 📄asgi.py
            └── 📄routing1.py
```

```py
# See also:
#     📖 [GitHub andrewgodwin/channels-examples/multichat/chat/consumers.py](https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py)
#     📖 [Python WebSocket通信の仕方：クライアント編](https://www.raspberrypirulo.net/entry/websocket-client)
#     📖 [websocket-client - Examples](https://websocket-client.readthedocs.io/en/latest/examples.html)
#     📖 [GitHub - websocket-client](https://github.com/websocket-client/websocket-client)
import sys
import traceback
import websocket

try:
    import thread  # 見つからない
except ImportError:
    import _thread as thread  # websocket-client の GitHub ではこっちが使われている

import time
import argparse
from main_finally import MainFinally


class Client2():

    def __init__(self, url):

        # デバックログの表示/非表示設定
        websocket.enableTrace(True)

        # WebSocketAppクラスを生成
        self.websockApp = websocket.WebSocketApp(url,
                                                 on_open=lambda ws: self.on_open(
                                                     ws),
                                                 on_close=lambda ws, close_status_code, close_msg: self.on_close(
                                                     ws, close_status_code, close_msg),
                                                 on_message=lambda ws, msg: self.on_message(
                                                     ws, msg),
                                                 on_error=lambda ws, msg: self.on_error(ws, msg))

    def on_message(self, ws, message):
        """メッセージ受信に呼ばれる関数"""
        print("receive : {}".format(message))

    def on_error(self, ws, error):
        """エラー時に呼ばれる関数"""
        print("### error ###")
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        """サーバーから切断時に呼ばれる関数"""
        print("### closed ###")

    def on_open(self, ws):
        """サーバーから接続時に呼ばれる関数"""
        thread.start_new_thread(self.run_worker, ())

    def run_worker(self, *args):
        """サーバーから接続時にスレッドで起動する関数"""
        while True:
            time.sleep(0.1)
            input_data = input("send JSON:")
            self.websockApp.send(input_data)

    def clean_up(self):
        self.websockApp.close()
        print("thread terminating...")

    def run_forever(self):
        """websocketクライアント起動"""
        self.websockApp.run_forever()


# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    class Main1:
        def __init__(self):
            self._client = None

        def on_main(self):
            parser = argparse.ArgumentParser(
                description='サーバーのアドレスとポートを指定して、テキストを送信します')
            parser.add_argument('--host', default="127.0.0.1",
                                help='サーバーのホスト。規定値:127.0.0.1')
            parser.add_argument('--port', type=int,
                                default=8000, help='サーバーのポート。規定値:8000')
            args = parser.parse_args()

            # FIXME このURLの埋め込みを外に出せないか？
            url = f"ws://{args.host}:{args.port}/websock-practice2/v1/"
            #                                    ---------------------
            #                                    1
            # 1. URLを合わせるように注意
            self._client = Client2(url)
            self._client.run_forever()
            return 0

        def on_except(self, e):
            """ここで例外キャッチ"""
            traceback.print_exc()

        def on_finally(self):
            if self._client:
                self._client.clean_up()

            print("★これで終わり")
            return 1

    sys.exit(MainFinally.run(Main1()))
```

# Step 8. コマンド実行

```shell
cd host_local1/websockapp1

python.exe -m client2
#             -------
#             1
# 1. Pythonファイル名。拡張子抜き
```

これで サーバー側とつながったはずだ。  
適当なJSON形式の文字列 `{"x":1}` でも打鍵してほしい。  
JSON形式として ふさわしくない文字列を送信するとサーバーが止まってしまう。  

サーバー側、クライアント側ともに `[ctrl] + [C]` キーで終了する。  

# 次の記事

📖 [Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！](https://qiita.com/muzudho1/items/3bd5e55fbea2c0598e8b)  

# 参考にした記事

📖 [Python WebSocket通信の仕方：クライアント編](https://www.raspberrypirulo.net/entry/websocket-client)  
📖 [websocket-client - Examples](https://websocket-client.readthedocs.io/en/latest/examples.html)  
📖 [GitHub - websocket-client](https://github.com/websocket-client/websocket-client)  
📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)  
📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  
📖 [Python で終了時に必ず何か実行したい](https://qiita.com/qualitia_cdev/items/f536002791671c6238e3)  
📖 [Django を WebSocket サーバにする](https://qiita.com/ekzemplaro/items/a6b81bd1d181fdd0cc24)  
📖 [django-channels を使った websocket を用いたチャットアプリの作成](https://zenn.dev/y_k/articles/e8878460fff3d5aa1d1d)  
📖 [Django ChannelsでできるリアルタイムWeb](https://qiita.com/massa142/items/cbd508efe0c45b618b34)  
📖 [GitHub andrewgodwin/channels-examples/multichat/chat/consumers.py](https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py)  
