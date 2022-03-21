"""
ASGI config for webapp1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
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
    "http": get_asgi_application(),  # 追加
    "websocket": AuthMiddlewareStack(  # 追加
        URLRouter(
            webapp1.routing1.websocket_urlpatterns
            # -----
            # 1
            #
            # 1. アプリケーション フォルダー名
        )
    ),
})
