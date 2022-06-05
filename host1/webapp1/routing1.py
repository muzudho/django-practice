# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url

# Websock練習１
from webapp1.websocks.websock_practice1.v1.consumer import WebsockPractice1V1Consumer
#    ------- ----------------------------- --------        --------------------------
#    1       2                             3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# Websock練習２
from webapp1.websocks.websock_practice2.v1.consumer import WebsockPractice2V1Consumer
#                                     ^                                   ^
#    ------- ----------------------------- --------        --------------------------
#    1       2                             3               4
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
from webapp1.websocks.tic_tac_toe.v2.consumer_custom import TicTacToeV2ConsumerCustom
#                                  ^ two                              ^ two
#    ------- ----------------------- ---------------        -------------------------
#    1       2                       3                      4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


websocket_urlpatterns = [

    # +----
    # | Websock練習１

    # Websock練習１
    url(r'^websock-practice1/v1/$', WebsockPractice1V1Consumer.as_asgi()),
    #     -----------------------   ------------------------------------
    #     1                                      2
    # 1. URLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする

    # | Websock練習１
    # +----




    # +----
    # | Websock練習２

    # Websock練習２
    url(r'^websock-practice2/v1/$', WebsockPractice2V1Consumer.as_asgi()),
    #                      ^                       ^
    #     -----------------------   ------------------------------------
    #     1                                      2
    # 1. URLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする

    # | Websock練習２
    # +----




    # 〇×ゲームの練習１
    url(r'^tic-tac-toe/v1/playing/(?P<room_name>\w+)/$',
        # --------------------------------------------
        # 1
        TicTacToeV1Consumer.as_asgi()),
    #   -----------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v1/playing/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方。
    #    room_name は変数として渡される
    # 2. クラス名とメソッド。 URL を ASGI形式にする

    # 〇×ゲームの練習２
    url(r'^tic-tac-toe/v2/playing/(?P<kw_room_name>\w+)/$',
        #               ^
        # -----------------------------------------------
        # 1
        TicTacToeV2ConsumerCustom.as_asgi()),
    #             ^
    #   -----------------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/playing/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方。
    #    kw_room_name は変数として渡される
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
