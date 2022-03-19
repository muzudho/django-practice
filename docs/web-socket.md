📖 [Django を WebSocket サーバにする](https://qiita.com/ekzemplaro/items/a6b81bd1d181fdd0cc24)  
📖 [django-channels を使った websocket を用いたチャットアプリの作成](https://zenn.dev/y_k/articles/e8878460fff3d5aa1d1d)  
📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  
📖 [Django ChannelsでできるリアルタイムWeb](https://qiita.com/massa142/items/cbd508efe0c45b618b34)  

# Step 1. requirements.txt ファイルの設定

ファイルの末尾にでも追加してほしい。  

📄host1/requirements.txt:  

```shell
# For web socket
channels>=3.0
```

# Step 2. settings.py ファイルの編集

そしたら、以下の部分を編集してほしい。  
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

# Step 3. asgi.py ファイルを編集＜その１＞

以下のファイルを編集してほしい。  

📄`host1/webapp1/asgi.py`:  

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

📄`host1/webapp1/websock1/consumer1.py`:  

```py
# See also:
#     📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
#     📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class Websock1Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = 'room1'
        self.room_group_name = f'{self.room_name}_group1'

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
        doc = json.loads(text_data)
        message = doc.get("message", None)

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'message': message,
        })

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
```

# Step 6. routing1.py ファイルを作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/websock1/routing1.py`:  

```py
# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url
from webapp1.websock1.consumer1 import Websock1Consumer

websocket_urlpatterns = [
    url(r'^websock1/$', Websock1Consumer.as_asgi()),
]
```

# Step 7. asgi.py ファイルの編集＜その２＞

`asgi.py` ファイルは既存なので、以下の部分をマージしてほしい。  

📄host1/webapp1/asgi.py:  

```py
import os

from django.core.asgi import get_asgi_application           # 削除の取消
# （削除） import django
# （削除） from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack               # 追加
from channels.routing import ProtocolTypeRouter, URLRouter  # 追加
import webapp1.websock1.routing1
#      ------- -------- --------
#      1       2        3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Pythonファイル名（拡張子除く）

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
            webapp1.websock1.routing1.websocket_urlpatterns
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

# WIP
