"""
ASGI config for webapp1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

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
