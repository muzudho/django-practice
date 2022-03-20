---
title: DjangoのWebサーバーとクライアント側のアプリ間でJSON形式のテキストを通信しよう！
tags: Django Docker JSON websocket アプリ
author: muzudho1
slide: false
---
# 目的

Webサーバーとクライアント間でテキストを双方向の非同期通信するのは前にやった。  
今回は送受信するデータが JSON形式 しかないと割り切ってみる。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                                                           | Value                                                                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Webサーバーとクライアント側のアプリで通信する方法を知っておく | 📖[DjangoのWebサーバーとクライアント側のアプリで通信しよう！](https://qiita.com/muzudho1/items/9bad88a4092bf83a0f12) |

この記事のアーキテクチャ:  

| Key              | Value                                     |
| ---------------- | ----------------------------------------- |
| OS               | Windows10                                 |
| Container        | Docker                                    |
| Web framework    | Django                                    |
| Communication    | JSON                                      |
| Program Language | Python 3                                  |
| Others           | Socket                                    |
| Editor           | Visual Studio Code （以下 VSCode と表記） |

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
├── 📂host_local1
│    └── 📂websockapp1
│        ├── 📄main_finally.py
│        └── 📄websock_client.py
└── 📂host1
     ├── 📂data
     │　　└── 📂db
     │         └── <たくさんのもの>
     ├── 📂webapp1
     │　　├── 📂templates
     │　　├── 📂websock1
     │　　│    └── consumer1.py
     │　　├── 📄asgi.py
     │　　├── 📄models.py
     │　　├── 📄routing1.py
     │　　├── 📄settings.py
     │　　├── 📄urls.py
     │　　└── <いろいろ>
     ├── 📄.env
     ├── 🐳docker-compose.yml
     ├── 🐳Dockerfile
     ├── 📄manage.py
     ├── 📄requirements.txt
     └── <いろいろ>
```

# Step 1. requirements.txt ファイルの編集

（無ければ）ファイルの末尾にでも追加してほしい。  

📄host1/requirements.txt:  

```shell
# （追加） For web socket
channels>=3.0
```

# Step 2. settings.py ファイルの編集

（無ければ）以下の部分を編集してほしい。  
`WSGI` から `ASGI` に乗り換えることをやっている。 `ASGI` は `WSGI` を兼ねるようだ。  

📄host1/webapp1/settings.py:  

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
# （追加）
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

# Step 3. asgi.py ファイルを編集

無ければ以下のファイルを作成、あればマージしてほしい。  

📄`host1/webapp1/asgi.py`:  

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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp1.settings')
#                                                -------
#                                                1
# 1. アプリケーション フォルダー名

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

# Step 5. consumer2.py ファイルを作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/websock1/consumer2.py`:  

```py
# See also:
#     📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
#     📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
#     📖 [Channels - Channel Layers](https://channels.readthedocs.io/en/stable/topics/channel_layers.html)
from channels.generic.websocket import AsyncJsonWebsocketConsumer
#                                           ----
#                                           1
# 1. Json を使うものに変更


class Consumer2(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")

    async def receive_json(self, doc):
        """
        Receive JSON from WebSocket.
        And format check automatically.
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

# Step 6. routing1.py ファイルを作成

無ければ以下のファイルを作成、あればマージしてほしい。  

📄`host1/webapp1/routing1.py`:  

```py
# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url
from webapp1.websock1.consumer2 import Consumer2 # 追加
#    ------- -------- ---------
#    1       2        3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

websocket_urlpatterns = [
    # （追加）
    url(r'^websock1-2/$', Consumer2.as_asgi()),
    #     -------------
    #     1
    # 1. URLの一部
]
```

# Step 7. Dockerコンテナの起動

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

# Step 8. ローカルPCにPythonのパッケージ websocket-client をインストール

Step 1 ～ 8. は サーバーサイドだった。  
Step 9. からは クライアントサイドを説明する。  

（もうしているかもしれないが）あなたのPCでコマンドを打鍵してほしい。  

```shell
pip install websocket-client
```

# Step 9. main_finally.py ファイルを作成

（無ければ）以下のファイルを作成してほしい。  

```plaintext
├── 📂host_local1
│    └── 📂websockapp1
│        └── 📄main_finally.py  # ここに新規作成
└── 📂host1                     # 既存
         ├── 📂data
         ├── 📂webapp1
         └── <いろいろ>
```

📄`host_local1/websockapp1/main_finally.py` （再掲）:  

```py
import sys
import signal


class MainFinally:
    """アプリケーション終了時に、必ず終了処理を実行するための仕掛けです。
    See also: 📖 [Python で終了時に必ず何か実行したい](https://qiita.com/qualitia_cdev/items/f536002791671c6238e3)

    Examples
    --------
    import sys
    import traceback
    from .main_finally import MainFinally

    class Main1:
        def on_main(self):
            # ここで通常の処理
            return 0

        def on_except(self, e):
            # ここで例外キャッチ
            traceback.print_exc()

        def on_finally(self):
            # ここで終了処理
            return 1


    # このファイルを直接実行したときは、以下の関数を呼び出します
    if __name__ == "__main__":
        sys.exit(MainFinally.run(Main1()))
    """

    @classmethod
    def run(clazz, target):
        """アプリケーション終了時に必ず on_finally()メソッドを呼び出します。
        通常の処理は on_main()メソッドに書いてください

        Parameters
        ----------
        target : class
            on_main(), on_except(), on_finally()メソッドが定義されたクラスです
        """
        def sigterm_handler(_signum, _frame) -> None:
            sys.exit(1)

        # 強制終了のシグナルを受け取ったら、強制終了するようにします
        signal.signal(signal.SIGTERM, sigterm_handler)

        try:
            # ここで何か処理
            return_code = target.on_main()

        except Exception as e:
            # ここで例外キャッチ
            target.on_except(e)

        finally:
            # 強制終了のシグナルを無視するようにしてから、クリーンアップ処理へ進みます
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)

            # ここで終了処理
            return_code = target.on_finally()

            # 強制終了のシグナルを有効に戻します
            signal.signal(signal.SIGTERM, signal.SIG_DFL)
            signal.signal(signal.SIGINT, signal.SIG_DFL)

        return return_code
```

# Step 10. websock_client.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
├── 📂host_local1
│    ├── 📂sockapp1
│    └── 📂websockapp1
│        └── 📄client2.py        # ここに新規作成
│        ├── 📄main_finally.py
│        └── 📄websock_client.py
└── 📂host1                      # 既存
         ├── 📂data
         ├── 📂webapp1
         └── <いろいろ>
```

📄`host_local1/websockapp1/client2.py`:  

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

            url = f"ws://{args.host}:{args.port}/websock1-2/"
            #                                    ----------
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

# Step 11. コマンド実行

```shell
cd host_local1/websockapp1

python.exe -m client2
#             -------
#             1
# 1. Pythonファイル名。拡張子抜き
```

これで サーバー側とつながったはずだ。  
適当なJSON形式の文字列 `{"x"=1}` でも打鍵してほしい。  
JSON形式として ふさわしくない文字列を送信するとサーバーが止まってしまう。  

サーバー側、クライアント側ともに `[ctrl] + [C]` キーで終了する。  

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
