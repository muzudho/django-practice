# 目的

ゲーム対局部屋をモニターしたい  

* 一手指す毎に
  * 盤面を、現盤面で上書きする
  * 棋譜に１手分追加する

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    └── 📄<いろいろ>
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂models_helper
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   ├── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │   │   └── 📂practice
        │   │   │       └── 📄<いろいろ>.js
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂tic-tac-toe
        │   │           ├── 📂v1
        │   │           └── 📂v2
        │   │               └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📂practice
        │   │       └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄urls.py
        │   └── 📄<いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        └── 📄urls.py
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 通信プロトコル作成 - message_converter.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v3o1
👉                      └── message_converter.py
```

```py
from asgiref.sync import sync_to_async

from webapp1.websocks.tic_tac_toe.v2.message_converter import TicTacToeV2MessageConverter
#                                  ^ two                                ^ two
#    ------- ----------------------- -----------------        ---------------------------
#    1       2                       3                        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV3o1MessageConverter(TicTacToeV2MessageConverter):
    """サーバープロトコル"""

    def on_end(self, scope, doc_received):
        """対局終了時"""
        pass

    async def on_move(self, scope, doc_received):
        """駒を置いたとき"""

        # ログインしていなければ AnonymousUser
        user = scope["user"]
        print(
            f"[TicTacToeV3o1MessageConverter on_move] user=[{user}] doc_received={doc_received}")
        if user.is_anonymous:
            # ログインしていないユーザーの操作は記録しません
            return

        # 部屋名
        #
        # * URLのパスに含まれている
        room_name = scope["url_route"]["kwargs"]["kw_room_name"]
        # print(f"[TicTacToeV3o1MessageConverter on_move] scope={scope}")

        # `c2s_` は クライアントからサーバーへ送られてきた変数の目印
        event = doc_received.get("c2s_event", None)
        # 駒を置いたマス番号
        sq = doc_received.get("c2s_sq", None)
        # 駒を置いた方の X か O
        piece_moved = doc_received.get("c2s_pieceMoved", None)
        print(
            f"[TicTacToeV3o1MessageConverter on_move] クライアントからのメッセージを受信しました room_name=[{room_name}] event=[{event}] piece_moved=[{piece_moved}] sq=[{sq}]")
        # クライアントからのメッセージを受信しました room_name=[Elephant] event=[C2S_Moved] piece_moved=[X] sq=[2]

        # 部屋取得
        room = await get_room_by_name(room_name)

        # （デバッグ）現状を出力
        print(
            f"[TicTacToeV3o1MessageConverter on_move] room=[{room}]")
        print(
            f"[TicTacToeV3o1MessageConverter on_move] now room.name=[{room.name}] room.board=[{room.board}] room.record=[{room.record}]")

        # 駒を置きます
        #
        # * 盤が9マスになるように右を '.' で埋めます
        room.board = room.board.ljust(9, '.')
        print(
            f"[TicTacToeV3o1MessageConverter on_move] now2 room.board=[{room.board}]")

        room.board = f"{room.board[:sq]}{piece_moved}{room.board[sq+1:]}"
        print(
            f"[TicTacToeV3o1MessageConverter on_move] now3 room.board=[{room.board}]")

        # 棋譜を書きます
        #
        # * 相手が AnonymousUser なら、相手の指し手が記録されていないものになります
        # * 9文字を超えるようなら、切り捨てます

        print(
            f"[TicTacToeV3o1MessageConverter on_move] now4 room.record=[{room.record}]")
        room.record = f"{room.record}{sq}"[:9]
        print(
            f"[TicTacToeV3o1MessageConverter on_move] now5 room.record=[{room.record}]")

        # 部屋を上書きします
        await save_room(room)

        print(f"[TicTacToeV3o1MessageConverter on_move] saved")

    def on_start(self, scope, doc_received):
        """対局開始時"""

        print(
            f"[TicTacToeV3o1MessageConverter on_start] ignored. doc_received={doc_received}")
        pass


@sync_to_async
def get_room_by_name(name):
    # FIXME 部屋名はIDではないので、先頭の要素を取得
    return Room.objects.filter(name=name)[0]


@sync_to_async
def save_room(room):
    room.save()
```

# Step 3. Webソケットの通信プロトコル作成 - consumer_custom.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v3o1
👉                      ├── consumer_custom.py
                        └── message_converter.py
```

```py
from webapp1.websocks.tic_tac_toe.v2.consumer_base import TicTacToeV2ConsumerBase
#                                  ^ two                            ^ two
#    ------- ----------------------- -------------        -----------------------
#    1       2                       3                    4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.websocks.tic_tac_toe.v3o1.message_converter import TicTacToeV3o1MessageConverter
#                                  ^^^ three o one                        ^^^ three o one
#    ------- ------------------------- -----------------        -----------------------------
#    1       2                         3                        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV3o1ConsumerCustom(TicTacToeV2ConsumerBase):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()
        self._messageConverter = TicTacToeV3o1MessageConverter()
        #                                  ^^^ three o one

    async def on_receive(self, doc_received):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """

        return await self._messageConverter.on_receive(self.scope, doc_received)
```

# Step 4. ルート編集 - routing1.py ファイル

以下の既存のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v3o1
            │           ├── consumer_custom.py
            │           └── message_converter.py
👉          └── routing1.py
```

```py
# 〇×ゲームの練習３．１
from webapp1.websocks.tic_tac_toe.v3o1.consumer_custom import TicTacToeV3o1ConsumerCustom
#                                  ^^^ three o one                      ^^^ three o one
#    ------- ------------------------- ---------------        ---------------------------
#    1       2                         3                      4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# ...中略...

websocket_urlpatterns = [

    # ...中略...

    # 〇×ゲームの練習３．１
    url(r'^tic-tac-toe/v3o1/playing/(?P<kw_room_name>\w+)/$',
        #               ^^^ three o one
        # -------------------------------------------------
        # 1
        TicTacToeV3o1ConsumerCustom.as_asgi()),
    #             ^^^ three o one
    #   -------------------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/playing/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方。
    #                              -----------------------------------
    #    kw_room_name は変数として渡される
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
```

# Step 5. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v3o1
            │           ├── consumer_custom.py
            │           └── message_converter.py
            ├── 📂views
            │   └── 📂tic_tac_toe
            │       └── 📂v3o1
👉          │           └── resources.py
            └── routing1.py
```

```py
"""〇×ゲームの練習３．１"""
from webapp1.views.tic_tac_toe.v2 import resources as tic_tac_toe_v2
#                               ^ two                              ^ two
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v3 import resources as tic_tac_toe_v3
#                               ^ three                            ^ three
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名


class MatchApplication():
    """対局申込ページ"""

    _path_of_http_playing = "/tic-tac-toe/v3o1/playing/{0}/?&myturn={1}"
    #                                      ^^^ three o one
    #                        ------------------------------------------
    #                        1
    # 1. http://example.com:8000/tic-tac-toe/v3o1/playing/Elephant/?&myturn=X
    #                           ---------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                     ^ two
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        return tic_tac_toe_v2.render_match_application(request, MatchApplication._path_of_http_playing, MatchApplication._path_of_html, MatchApplication.on_sent, MatchApplication.open)
        #                   ^ two

    @staticmethod
    def on_sent(request):
        """送信後"""
        return tic_tac_toe_v3.match_application_on_sent(request)

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return tic_tac_toe_v2.match_application_open_context
        #                   ^ two


class Playing():

    _path_of_ws_playing = "/tic-tac-toe/v3o1/playing/"
    #                                    ^^^ three o one
    #                      --------------------------
    #                      1
    # 1. ws://example.com/tic-tac-toe/v3o1/playing/Elephant/
    #                    --------------------------

    _path_of_html = "webapp1/tic-tac-toe/v3/playing.html.txt"
    #                                     ^ three
    #                ---------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/playing.html.txt
    #                            ---------------------------------------

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        return tic_tac_toe_v2.render_playing(
            #               ^ two
            request,
            kw_room_name,
            Playing._path_of_ws_playing,
            Playing._path_of_html,
            Playing.on_update,
            tic_tac_toe_v2.playing_expected_pieces)
        #                ^ two

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass
```

# Step 6. ルート編集 - urls.py ファイル

以下の既存のファイルに、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂websocks
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v3o1
        │   │           ├── consumer_custom.py
        │   │           └── message_converter.py
        │   ├── 📂views
        │   │   └── 📂tic_tac_toe
        │   │       └── 📂v3o1
        │   │           └── resources.py
        │   ├── routing1.py
👉      │   └── 📄urls.py                       # こちら
❌      └── 📄urls.py                           # これではない
```

👇追加する部分のみ抜粋

```py
from webapp1.views.tic_tac_toe.v3o1 import resources as tic_tac_toe_v3o1
#    ------- ----------------------        ---------    ----------------
#    1       2                             3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [

    # ...中略...

    # +----
    # | 〇×ゲーム３．１

    # 対局申込
    path('tic-tac-toe/v3o1/match-application/',
         #             ^^^
         # ----------------------------------
         # 1
         tic_tac_toe_v3o1.MatchApplication.render),
    #                 ^^^
    #    ----------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. tic_tac_toe_v3o1 (別名)ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3o1/playing/<str:kw_room_name>/',
         #             ^^^
         # -------------------------------------------
         # 1
         tic_tac_toe_v3o1.Playing.render),
    #                 ^^^
    #    -------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v3o1 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３．１
    # +----
]
```

# Step 7. Web画面へアクセス

* このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください
* テストするためには `サインアップ` してアカウントを作ってから、 `ログイン` してください
* 最初のテストは　既存でない部屋名で、次のテストは　既存の部屋名　で行うといいかもしれません

📖 [http://localhost:8000/accounts/v1/signup/](http://localhost:8000/accounts/v1/signup/)  
📖 [http://localhost:8000/accounts/v1/login/](http://localhost:8000/accounts/v1/login/)  
📖 [http://localhost:8000/tic-tac-toe/v3o1/match-application/](http://localhost:8000/tic-tac-toe/v3o1/match-application/)  

部屋、ユーザーを確認するには、管理画面を使うのが確実です:  

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

# 次の記事

📖 [Djangoで観戦モードを作ろう！](https://qiita.com/muzudho1/items/9e4a7dd1ccfac6ac8d66)  

# 参考にした記事

## 非同期処理，スレッド関連

📖 [Django: SynchronousOnlyOperation: You cannot call this from an async context - use a thread or sync_to_async](https://stackoverflow.com/questions/61926359/django-synchronousonlyoperation-you-cannot-call-this-from-an-async-context-u)  
📖 [Asynchronous support](https://docs.djangoproject.com/en/4.0/topics/async/)  
📖 [How to correct " 'coroutine' object has no attribute 'data'" Error when using Telethon for Telegram?](https://stackoverflow.com/questions/57147419/how-to-correct-coroutine-object-has-no-attribute-data-error-when-using-te)  
📖 [python3 の async/awaitを理解する](https://qiita.com/maueki/items/8f1e190681682ea11c98)  
📖 [Getting values from functions that run as asyncio tasks](https://stackoverflow.com/questions/32456881/getting-values-from-functions-that-run-as-asyncio-tasks)  

## 文字列関連

📖 [Python で文字列の一文字だけを変換](https://iatlex.com/python/string_change_1str)  
