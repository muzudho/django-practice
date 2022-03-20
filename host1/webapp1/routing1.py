# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url
from webapp1.websock1.consumer1 import Websock1Consumer
from webapp1.websock1.consumer2 import Consumer2  # 追加
#    ------- -------- ---------
#    1       2        3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

websocket_urlpatterns = [
    url(r'^websock1/$', Websock1Consumer.as_asgi()),

    # （追加）
    url(r'^websock1-2/$', Consumer2.as_asgi()),
    #     -------------
    #     1
    # 1. URLの一部
]
