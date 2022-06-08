# 目的

ゲーム対局部屋をモニターしたい  

* 対局開始時に、初期盤面を保存する。棋譜は空っぽにする
* 一手指す毎に、現盤面で上書きする。棋譜に１手分追加する

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
        │   │       ├── 📂tic-tac-toe
        │   │       │   ├── 📂v1
        │   │       │   └── 📂v2
        │   │       │       └── 📄<いろいろ>.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── 📄<いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── 📄<いろいろ>
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 通信プロトコル作成 - protocol.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v3o1
👉                      └── protocol.py
```

```py
from webapp1.websocks.tic_tac_toe.v2.protocol import TicTacToeV2Protocol
#                                  ^ two                       ^ two
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
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


class TicTacToeV3o1Protocol(TicTacToeV2Protocol):
    """サーバープロトコル"""

    def on_end(self, request):
        """対局終了時"""
        pass

    def on_move(self, request):
        """石を置いたとき"""

        sq = request.get("sq", None),
        # my_piece = request.get("myPiece", None),
        print(
            f"[TicTacToeV3o1Protocol on_move] sq=[{sq}]")

        # `po_` は POST送信するパラメーター名の目印
        # 部屋名
        po_room_name = request.POST.get("po_room_name")
        # 自分の駒。 X か O
        po_my_piece = request.POST.get("po_my_piece")
        print(
            f"[TicTacToeV3o1Protocol on_move] po_room_name=[{po_room_name}] po_my_piece=[{po_my_piece}]")

        # 部屋の取得 または 新規作成
        #
        # * ID ではなく、部屋名から行う
        room_table_qs = Room.objects.filter(name=po_room_name)
        print(
            f"[TicTacToeV3o1Protocol on_move] len(room_table_qs)={len(room_table_qs)}")

        if 1 == len(room_table_qs):
            # FIXME 名前被りの部屋が存在すると正しく動きません
            room = room_table_qs[0]
        else:
            raise ValueError(f"room fail. po_room_name=[{po_room_name}]")

        # （デバッグ）現状を出力
        print(
            f"[TicTacToeV3o1Protocol on_move] now room.board=[{room.board}] room.record=[{room.record}]")

        # TODO room.board 文字列に石を追加したい
        # TODO room.record 文字列に座標を追加したい

        pass

    def on_start(self, request):
        """対局開始時"""
        pass
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
                        └── protocol.py
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

from webapp1.websocks.tic_tac_toe.v3o1.protocol import TicTacToeV3o1Protocol
#                                  ^^^ three o one               ^ three o one
#    ------- ----------------------- ----------        ---------------------
#    1       2                       3                 4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV3o1ConsumerCustom(TicTacToeV2ConsumerBase):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()
        self._protocol = TicTacToeV3o1Protocol()
        #                          ^^^ three o one

    def on_receive(self, request):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """
        return self._protocol.execute(request)
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
            │           └── protocol.py
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

# Step 5. ビュー編集 - v_tic_tac_toe_v3o1.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v3o1
            │           ├── consumer_custom.py
            │           └── protocol.py
            ├── 📂views
👉          │   └── v_tic_tac_toe_v3o1.py
            └── routing1.py
```

```py
from webapp1.views.v_tic_tac_toe_v3 import MatchApplication as MatchApplicationV3
#    ------- ----- ----------------        ----------------    ------------------
#    1       2     3                       4                   5
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名
# 5. `4.` に付けた別名

from webapp1.views.v_tic_tac_toe_v3 import Playing as PlayingV3
#    ------- ----- ----------------        -------    ---------
#    1       2     3                       4          5
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名
# 5. `4.` に付けた別名


class MatchApplication(MatchApplicationV3):
    """対局申込ページ"""

    path_of_playing = "/tic-tac-toe/v3o1/playing/{0}/?&mypiece={1}"
    #                                ^^^ three o one
    #                  -------------------------------------------
    #                  1
    # 1. http://example.com:8000/tic-tac-toe/v3o1/playing/Elephant/?&mypiece=X
    #                           ----------------------------------------------

    path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                    ^ two
    #               ---------------------------------------------
    #               1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------


class Playing(PlayingV3):

    path_of_playing = "/tic-tac-toe/v3o1/playing/"
    #                                ^^^ three o one
    #                  --------------------------
    #                  1
    # 1. http://example.com/tic-tac-toe/v3o1/playing/Elephant/
    #                      --------------------------
```

# Step 6. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v3o1
            │           ├── consumer_custom.py
            │           └── protocol.py
            ├── 📂views
            │   └── v_tic_tac_toe_v3o1.py
            ├── routing1.py
👉          └── urls.py
```

👇追加する部分のみ抜粋

```py
from webapp1.views import v_tic_tac_toe_v3o1
#    ------- -----        ------------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [

    # ...中略...

    # +----
    # | 〇×ゲーム３

    # ...中略...

    # 対局申込
    path('tic-tac-toe/v3o1/match-application/',
         #             ^^^
         # ----------------------------------
         # 1
         v_tic_tac_toe_v3o1.MatchApplication.render),
    #                   ^^^
    #    ------------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. v_tic_tac_toe_v3o1.py ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3o1/playing/<str:kw_room_name>/',
         #             ^^^
         # -------------------------------------------
         # 1
         v_tic_tac_toe_v3o1.Playing.render),
    #                   ^^^
    #    ---------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. v_tic_tac_toe_v3o1.py ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３
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
