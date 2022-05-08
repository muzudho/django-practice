# 目的

Webサーバーとクライアント間で双方向の非同期通信をしたい。だからする。  
その手法の１つの **Webソケット** ならできる。  

# はじめに

前提知識:  

| Key                  | Value                                                                        |
| -------------------- | ---------------------------------------------------------------------------- |
| ソケットを知っておく | 📖[ソケットを使おう！](https://qiita.com/muzudho1/items/7a6501f7dbafbaa9b96c) |

この記事のアーキテクチャ:  

| Key              | Value                                     |
| ---------------- | ----------------------------------------- |
| OS               | Windows10                                 |
| Container        | Docker                                    |
| Program Language | Python 3                                  |
| Others           | Web socket                                |
| Editor           | Visual Studio Code （以下 VSCode と表記） |

この記事は Lesson01 から続いていて、順にやってこないと ソースが足りず実行できないので注意されたい。  

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    └── 📂sockapp1
    │        ├── 📄client.py
    │        ├── 📄echo_server.py
    │        └── 📄main_finally.py
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   └── 📂vuetify-practice
        │   │       └── 📄desserts.json
        │   ├── 📂templates
        │   │   └── 📂<いろいろ>-practice
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📄admin.py
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

# Step 1. プログラミング環境の編集 - requirements.txt ファイル

以下のファイルに追加してほしい。末尾で構わない。  

```plaintext
    └── 📂host1
👉      └── 📄requirements.txt
```

```shell
# For web socket
channels>=3.0
```

# Step 2. 設定の編集 - settings.py ファイル

そしたら、以下の部分を編集してほしい。  
`WSGI` から `ASGI` に乗り換えることをやっている。 `ASGI` は `WSGI` を兼ねるようだ。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
👉      │   └── 📄settings.py
        └── 📄requirements.txt
```

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # （追加） For web socket
    'channels',
]

# （削除） WSGI_APPLICATION = 'webapp1.wsgi.application'
ASGI_APPLICATION = "webapp1.asgi.application"
#                   -------
#                   1
# 1. アプリケーション フォルダー名

# （追加） See also: 📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
CHANNEL_LAYERS = {
    'default': {
        ### Method 1: Via redis lab
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [
        #       'redis://h:<password>;@<redis Endpoint>:<port>' 
        #     ],
        # },

        ### Method 2: Via local Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #      "hosts": [('127.0.0.1', 6379)],
        # },

        ### Method 3: Via In-memory channel layer
        ## Using this method.
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
```

# Step 3. 設定の編集 - asgi.py ファイル＜その１＞

以下のファイルを編集してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
👉      │   ├── 📄asgi.py
        │   └── 📄settings.py
        └── 📄requirements.txt
```

```py
import os

# （削除） from django.core.asgi import get_asgi_application
import django                                   # 追加
from channels.http import AsgiHandler           # 追加
from channels.routing import ProtocolTypeRouter # 追加

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp1.settings')
#                                                -------
#                                                1
# 1. アプリケーション フォルダー名

django.setup() # 追加

# （削除） application = get_asgi_application()
application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  ## IMPORTANT::Just HTTP for now. (We can add other protocols later.)
})
```

# Step 4. コマンド実行

Dockerコンテナは停止しているものとし、以下のコマンドを打鍵してほしい。  

```shell
# requirements.txt を編集したので ビルドし直します
docker-compose build

# settings.py を編集したのでマイグレーションし直します
docker-compose run --rm web python3 manage.py migrate

# 起動
docker-compose up
```

# Step 5. consumer1.py ファイルを作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂websock1
👉      │   │   └── 📄consumer1.py
        │   ├── 📄asgi.py
        │   └── 📄settings.py
        └── 📄requirements.txt
```

```py
# See also:
#     📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
#     📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
#     📖 [Channels - Channel Layers](https://channels.readthedocs.io/en/stable/topics/channel_layers.html)
from channels.generic.websocket import AsyncWebsocketConsumer

class Websock1Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        """
        print("Received")
        # Send message to WebSocket
        await self.send(text_data=f"Echo: {text_data}")

    async def send_message(self, res):
        """ Receive message from room group """
        print("Sent message")
        # Send message to WebSocket
        await self.send(text_data=res)
```

# Step 6. routing1.py ファイルを作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂websock1
        │   │   └── 📄consumer1.py
        │   ├── 📄asgi.py
👉      │   ├── 📄routing1.py
        │   └── 📄settings.py
        └── 📄requirements.txt
```

```py
# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url
from webapp1.websock1.consumer1 import Websock1Consumer

websocket_urlpatterns = [
    url(r'^websock1/$', Websock1Consumer.as_asgi()),
]
```

# Step 7. 設定の編集 - asgi.py ファイル＜その２＞

`asgi.py` ファイルは既存なので、以下の部分をマージしてほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂websock1
        │   │   └── 📄consumer1.py
👉      │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   └── 📄settings.py
        └── 📄requirements.txt
```

```py
import os

from django.core.asgi import get_asgi_application           # 削除の取消
# （削除） import django
# （削除） from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack               # 追加
from channels.routing import ProtocolTypeRouter, URLRouter  # 追加
import webapp1.routing1
#      ------- --------
#      1       2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp1.settings')
#                                                -------
#                                                1
# 1. アプリケーション フォルダー名

# （削除） django.setup()

# （削除） application = get_asgi_application()
application = ProtocolTypeRouter({
    # （削除） "http": AsgiHandler(),
    "http": get_asgi_application(), # 追加
    "websocket": AuthMiddlewareStack( # 追加
        URLRouter(
            webapp1.routing1.websocket_urlpatterns
        )
    ),
})
```

# Step 8. Dockerコンテナの起動

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

# Step 9. ローカルPCにPythonのパッケージ websocket-client をインストール

Step 1 ～ 8. は サーバーサイドだった。  
Step 9. からは クライアントサイドを説明する。  

あなたのPCでコマンドを打鍵してほしい。  

```shell
pip install websocket-client
```

# Step 10. 複製 - main_finally.py ファイル

以下の記事で掲載した main_finally.py ファイルを複製してほしい。  

* 📖 [ソケットを使おう！](https://qiita.com/muzudho1/items/7a6501f7dbafbaa9b96c)
  * 📄`host1/webapp1/static/vuetify-practice/desserts.json`

以下のファイルをコピー＆ペーストしてほしい。  

```plaintext
    ├── 📂host_local1
    │    ├── 📂sockapp1
👉  │    │   └── 📄main_finally.py  # ここからコピー
    │    └── 📂websockapp1
👉  │        └── 📄main_finally.py  # ここへペースト
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂websock1
        │   │   └── 📄consumer1.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   └── 📄settings.py
        └── 📄requirements.txt
```

# Step 11. websock_client.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    ├── 📂host_local1
    │    ├── 📂sockapp1
    │    │   └── 📄main_finally.py
    │    └── 📂websockapp1
    │        ├── 📄main_finally.py
👉  │        └── 📄websock_client.py
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂websock1
        │   │   └── 📄consumer1.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   └── 📄settings.py
        └── 📄requirements.txt
```

```py
# See also:
#     📖 [Python WebSocket通信の仕方：クライアント編](https://www.raspberrypirulo.net/entry/websocket-client)
#     📖 [websocket-client - Examples](https://websocket-client.readthedocs.io/en/latest/examples.html)
#     📖 [GitHub - websocket-client](https://github.com/websocket-client/websocket-client)
import sys
import traceback
import websocket

try:
    import thread # 見つからない
except ImportError:
    import _thread as thread # websocket-client の GitHub ではこっちが使われている

import time
import argparse
from main_finally import MainFinally

class Websocket_Client():

    def __init__(self, url):

        # デバックログの表示/非表示設定
        websocket.enableTrace(True)

        # WebSocketAppクラスを生成
        self.websockApp = websocket.WebSocketApp(url,
            on_open     = lambda ws: self.on_open(ws),
            on_close    =lambda ws, close_status_code, close_msg: self.on_close(ws, close_status_code, close_msg),
            on_message  = lambda ws, msg: self.on_message(ws, msg),
            on_error    = lambda ws, msg: self.on_error(ws, msg))


    def on_message(self, ws, message):
        """メッセージ受信に呼ばれる関数"""
        print("receive : {}".format(message))

    def on_error(self, ws, error):
        """エラー時に呼ばれる関数"""
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
            input_data = input("send data:") 
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
            parser.add_argument('--host', default="127.0.0.1", help='サーバーのホスト。規定値:127.0.0.1')
            parser.add_argument('--port', type=int, default=8000, help='サーバーのポート。規定値:8000')
            args = parser.parse_args()

            url = f"ws://{args.host}:{args.port}/websock1/"
            self._client = Websocket_Client(url)
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

# Step 12. コマンド実行

```shell
cd host_local1/websockapp1

python.exe -m websock_client
```

これで サーバー側とつながったはずだ。  
適当な文字列 `hello` でも打鍵してほしい。  
サーバー側、クライアント側ともに `[ctrl] + [C]` キーで終了する。  

# 次の記事

📖 [DjangoのWebサーバーとクライアント側のアプリ間でJSON形式のテキストを通信しよう！](https://qiita.com/muzudho1/items/a3870c78f609a65debe0)

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
