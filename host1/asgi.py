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

import apps1.tic_tac_toe.urls_ws1
#      ----------------- --------
#      1                 2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

import webapp1.routing1
#      ------- --------
#      1       2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

# 複数のアプリケーションの websocket_urlpatterns をマージします
websocket_urlpatterns_merged = []
websocket_urlpatterns_merged.extend(
    apps1.tic_tac_toe.urls_ws1.websocket_urlpatterns)
websocket_urlpatterns_merged.extend(webapp1.routing1.websocket_urlpatterns)

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

# （削除） django.setup()

# （削除） application = get_asgi_application()

application = ProtocolTypeRouter({
    # （削除） "http": AsgiHandler(),
    "http": get_asgi_application(),  # 追加
    "websocket": AuthMiddlewareStack(  # 追加
        URLRouter(
            # * 削除
            # webapp1.routing1.websocket_urlpatterns
            # * 追加
            websocket_urlpatterns_merged
        )
    ),
})
