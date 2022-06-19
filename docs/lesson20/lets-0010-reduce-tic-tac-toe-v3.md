# 目的

`Play Again` （再戦）するかどうかは、プレイヤーが選べるのではなく、サーバー側が選ぶようにしたい  
そこで `Play Again` ボタンを外す  

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

# Step 2. 対局画面作成 - playing.html.txt ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v3
👉                          └── playing.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "tic-tac-toe/v2/playing_base.html" %}
{#                       ^ two
            --------------------------------
            1
1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/playing_base.html
                                   --------------------------------

    自動フォーマットしないでください
    Do not auto fomatting
#}


{% block footer_section1 %}
    <!-- フッターにボタンを置きません -->
{% endblock footer_section1 %}


{% block methods_footer %}
    // フッターのボタンは除きました
{% endblock methods_footer %}
```

# Step 3. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v3
            │               └── playing.html.txt
            └── 📂views
                └── 📂tic_tac_toe
                    └── 📂v3
👉                      └── resources.py
```

```py
"""〇×ゲームの練習３"""
# from django.contrib.auth.models import User # デバッグ用

from webapp1.views.tic_tac_toe.v2 import resources as tic_tac_toe_v2
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名


class MatchApplication():
    """対局申込ページ"""

    _path_of_http_playing = "/tic-tac-toe/v3/playing/{0}/?&myturn={1}"
    #                                      ^ three
    #                        ----------------------------------------
    #                        1
    # 1. http://example.com:8000/tic-tac-toe/v3/playing/Elephant/?&myturn=X
    #                           -------------------------------------------

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
        # 拡張したい挙動があれば、ここに書く
        pass

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return tic_tac_toe_v2.match_application_open_context
        #                   ^ two


class Playing():
    """対局ページ"""

    _path_of_ws_playing = "/tic-tac-toe/v2/playing/"
    #                                    ^ two
    #                      ------------------------
    #                      1
    # 1. ws://example.com/tic-tac-toe/v2/playing/Elephant/
    #                    ------------------------

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

# Step 4. ルート編集 - urls.py ファイル

以下の既存のファイルに、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂tic-tac-toe
        │   │           └── 📂v3
        │   │               └── playing.html.txt
        │   ├── 📂views
        │   │   └── 📂tic_tac_toe
        │   │       └── 📂v3
        │   │           └── resources.py
👉      │   └── 📄urls.py                       # こちら
❌      └── 📄urls.py                           # これではない
```

👇追加する部分のみ抜粋

```py
from django.urls import path

from webapp1.views.tic_tac_toe.v3 import resources as tic_tac_toe_v3
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [
    # ...略...

    # +----
    # | 〇×ゲーム３

    # 対局申込
    path('tic-tac-toe/v3/match-application/',
         #             ^
         # --------------------------------
         # 1
         tic_tac_toe_v3.MatchApplication.render),
    #                 ^
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/match-application/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v3.py (別名)ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3/playing/<str:kw_room_name>/',
         #             ^
         # -----------------------------------------
         # 1
         tic_tac_toe_v3.Playing.render),
    #                 ^
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/playing/<部屋名>/` のような URL のパスの部分。
    #                              --------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v3.py (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３
    # +----
]
```

# Step 5. Web画面へアクセス

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください  

📖 [http://localhost:8000/tic-tac-toe/v3/match-application/](http://localhost:8000/tic-tac-toe/v3/match-application/)  

# 次の記事

📖 [Djangoでチェックインを作ろう！](https://qiita.com/muzudho1/items/1ce542dd66929d7bce3f)  
