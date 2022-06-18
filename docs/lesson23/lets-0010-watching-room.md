# 目的

観戦したい  

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

# Step 2. 対局画面作成 - playing.html.txt ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v3o2
👉                          └── playing.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "tic-tac-toe/v3/playing.html.txt" %}
{#                       ^ three
            -------------------------------
            1
1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/playing.html.txt
                                   -------------------------------

    自動フォーマットしないでください
    Do not auto fomatting
#}


{% block isYourTurn_patch1 %}
    // "X" か "O" かのどちらかのプレイヤーか
    isYourTurn = isYourTurn && (this.engine.position.turn.me == 'X' || this.engine.position.turn.me == 'O');
{% endblock isYourTurn_patch1 %}


{% block appendix_message %}
    xWin: "X win!",
    oWin: "O win!",
{% endblock appendix_message %}


{% block create_gameover_message %}
    // 観戦者のケース
    if (this.engine.position.turn.me == '_') {
        switch (this.engine.winner) {
            case PC_X_LABEL:
                return this.messages.xWin;
            case PC_O_LABEL:
                return this.messages.oWin;
            case PC_EMPTY_LABEL:
                return this.messages.draw;
            default:
                throw `unknown this.engine.winner = ${this.engine.winner}`;
        }
    }
{% endblock create_gameover_message %}
```

# Step 3. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v3o2
            │               └── playing.html.txt
            └── 📂views
                └── 📂tic_tac_toe
                    └── 📂v3o2
👉                      └── resources.py
```

```py
"""〇×ゲームの練習３．２"""
import json
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


# 以下、よく使う定型データ


# 対局申込 - 訪問後
match_application_open_context = {
    # `dj_` は Djangoでレンダーするパラメーター名の目印
    # 入場者データ
    "dj_visitor_value": "X",
    # Python と JavaScript 間で配列データを渡すために JSON 文字列形式にします
    "dj_visitor_select": json.dumps([
        {"text": "X", "value": "X"},
        {"text": "O", "value": "O"},
        {"text": "WatchingGame", "value": "_"},  # add
    ]),
}


# 対局中 - 駒
playing_expected_pieces = ['X', 'O', '_']


# 以下、ロジック


class MatchApplication():
    """対局申込ページ"""

    _path_of_http_playing = "/tic-tac-toe/v3o2/playing/{0}/?&myturn={1}"
    #                                    ^^^ three o two
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
        #                   ^ three

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return match_application_open_context
        #      ^ Located in this file


class Playing():

    _path_of_ws_playing = "/tic-tac-toe/v3o1/playing/"
    #                                    ^^^ three o one
    #                      --------------------------
    #                      1
    # 1. ws://example.com/tic-tac-toe/v3o1/playing/Elephant/
    #                    --------------------------

    _path_of_html = "webapp1/tic-tac-toe/v3o2/playing.html.txt"
    #                                     ^ three o two
    #                -----------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3o2/playing.html.txt
    #                            -----------------------------------------

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
            playing_expected_pieces)
        #   ^ Located in this file

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v3o2
            │               └── playing.html.txt
            ├── 📂views
            │   └── 📂tic_tac_toe
            │       └── 📂v3o2
            │           └── resources.py
👉          └── urls.py
```

👇追加する部分のみ抜粋

```py
from webapp1.views.tic_tac_toe.v3o2 import resources as tic_tac_toe_v3o2
#    ------- ----------------------        ---------    ----------------
#    1       2                             3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [

    # ...中略...

    # +----
    # | 〇×ゲーム３．２

    # 対局申込
    path('tic-tac-toe/v3o2/match-application/',
         #             ^^^ three o two
         # ----------------------------------
         # 1
         tic_tac_toe_v3o2.MatchApplication.render),
    #                 ^^^ three o two
    #    ----------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o2/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. tic_tac_toe_v3o2 (別名)ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3o2/playing/<str:kw_room_name>/',
         #             ^^^ three o two
         # -------------------------------------------
         # 1
         tic_tac_toe_v3o2.Playing.render),
    #                 ^^^
    #    -------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o2/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v3o2 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３．２
    # +----
]
```

# Step 5. Web画面へアクセス

* このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください
* テストするためには `サインアップ` してアカウントを作ってから、 `ログイン` してください
* 最初のテストは　既存でない部屋名で、次のテストは　既存の部屋名　で行うといいかもしれません

📖 [http://localhost:8000/accounts/v1/signup/](http://localhost:8000/accounts/v1/signup/)  
📖 [http://localhost:8000/accounts/v1/login/](http://localhost:8000/accounts/v1/login/)  
📖 [http://localhost:8000/tic-tac-toe/v3o2/match-application/](http://localhost:8000/tic-tac-toe/v3o2/match-application/)  

部屋、ユーザーを確認するには、管理画面を使うのが確実です:  

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  
