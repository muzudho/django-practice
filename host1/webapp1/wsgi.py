"""
WSGI config for webapp1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

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

application = get_wsgi_application()
