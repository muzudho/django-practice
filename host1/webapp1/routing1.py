# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url
from webapp1.websock1.consumer1 import Websock1Consumer

from webapp1.websock1.consumer2 import Consumer2
#    ------- -------- ---------        ---------
#    1       2        3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# 〇×ゲームの練習１
from webapp1.websocks.tic_tac_toe.v1.consumer import TicTacToeV1Consumer
#    ------- ----------------------- --------        -------------------
#    1       2                       3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# 〇×ゲームの練習２
from webapp1.websocks.tic_tac_toe.v2.consumer import TicTacToeV2Consumer
#                                  ^                           ^
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# 〇×ゲームの練習３
from webapp1.tic_tac_toe3.consumer1 import TicTacToe3Consumer1  # 追加
#                       ^                           ^
#    ------- ------------ ---------        -------------------
#    1       2            3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

websocket_urlpatterns = [
    url(r'^websock1/$', Websock1Consumer.as_asgi()),

    # （追加）
    url(r'^websock1-2/$', Consumer2.as_asgi()),
    #     -------------
    #     1
    # 1. URLの一部

    # 〇×ゲームの練習１
    url(r'^tic-tac-toe/v1/(?P<room_name>\w+)/$', TicTacToeV1Consumer.as_asgi()),
    #     ------------------------------------   -----------------------------
    #     1                                      2
    # 1. URLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする

    # 〇×ゲームの練習２
    url(r'^tic-tac-toe/v2/(?P<room_name>\w+)/$', TicTacToeV2Consumer.as_asgi()),
    #                 ^                                 ^
    #     ------------------------------------   -----------------------------
    #     1                                      2
    # 1. URLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする

    # 〇×ゲームの練習３
    url(r'^tic-tac-toe3/(?P<room_name>\w+)/$', TicTacToe3Consumer1.as_asgi()),
    #                 ^                                 ^
    #     ----------------------------------   -----------------------------
    #     1                                    2
    # 1. URLの一部（正規表現）の Django での書き方
    # 2. ASGI形式での書き方
]
