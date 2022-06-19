# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url

# 〇×ゲームの練習１
from apps1.tic_tac_toe.websocks.v1o1.consumer import TicTacToeV1Consumer
#    ----- ----------- ------------- --------        -------------------
#    1     2           3             4               5
#    ----------------------------------------
#    6
# 1. 開発者用ディレクトリーの一部
# 2. アプリケーション フォルダー名
# 3. ディレクトリー名
# 4. Python ファイル名。拡張子抜き
# 5. クラス名
# 6. モジュール名

websocket_urlpatterns = [
    # 〇×ゲームの練習１
    url(r'^tic-tac-toe/v1o1/playing/(?P<room_name>\w+)/$',
        # ----------------------------------------------
        # 1
        TicTacToeV1Consumer.as_asgi()),
    #   -----------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v1o1/playing/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方。
    #    room_name は変数として渡される
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
