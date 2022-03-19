# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url
from webapp1.websock1.consumer1 import Websock1Consumer

websocket_urlpatterns = [
    url(r'^websock1/$', Websock1Consumer.as_asgi()),
]
