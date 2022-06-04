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
        │   │   ├── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │   │   └── 📂practice
        │   │   │       └── 📄<いろいろ>.js
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂tic-tac-toe
        │   │       │   ├── 📂v1
        │   │       │   └── 📂v2
        │   │       │       ├── 📄match_request.html
        │   │       │       └── 📄play.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           ├── 📄consumer.py
        │   │           └── 📄protocol.py
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

# Step 2. 対局画面作成 - play.html.txt ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v3
👉                          └── play.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "tic-tac-toe/v2/play_base.html" %}
{#          -----------------------------
            1
1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/play_base.html
                                   -----------------------------

    自動フォーマットしないでください
    Do not auto fomatting
#}

{% block footer_section1 %}
                    <!-- フッターにボタンを置きません -->
{% endblock footer_section1 %}

{% block method_section1 %}
                    // フッターのボタンは除きました
{% endblock method_section1 %}
```

# Step 3. ビュー作成 - v_tic_tac_toe_v3.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v3
            │               └── play.html.txt
            └── 📂views
                └── v_tic_tac_toe_v3.py
```

```py
from django.http import Http404
from django.shortcuts import render, redirect


def render_match_request(request):
    """対局要求"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe/v3/play/{room_name}/?&mypiece={myPiece}')
        #                               ^ three
        #                 ----------------------------------------------------
        #                 1
        # 1. http://example.com:8000/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                           -----------------------------------------
    return render(request, "webapp1/tic-tac-toe/v2/match_request.html", {})
    #                                            ^ two
    #                       -----------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_request.html
    #                            -----------------------------------------


def render_play(request, room_name):
    """対局画面"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "webapp1/tic-tac-toe/v3/play.html.txt", context)
    #                                            ^ three
    #                       ------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/play.html.txt
    #                            ------------------------------------
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v3
            │               └── play.html.txt
👉          └── urls.py
```

👇追加する部分のみ抜粋

```py
from django.urls import path

from webapp1.views import v_tic_tac_toe_v3
#    ------- -----        ----------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...略...

    # 対局要求
    path('tic-tac-toe/v3/match-request/',
         #             ^
         # -----------------------------
         # 1
         v_tic_tac_toe_v3.render_match_request),
    #                   ^
    #    -------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/match-request/` のような URL のパスの部分
    #                              ------------------------------
    # 2. v_tic_tac_toe_v3.py ファイルの render_match_request メソッド

    # 対局中
    path('tic-tac-toe/v3/play/<str:room_name>/', v_tic_tac_toe_v3.render_play),
    #                  ^                                        ^
    #     ------------------------------------   ----------------------------
    #     1                                      2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/play/<部屋名>/` のような URL のパスの部分。 <部屋名> に入った文字列は room_name 変数に渡されます
    #                              -----------------------------
    # 2. v_tic_tac_toe_v3.py ファイルの render_play メソッド
]
```

# Step 5. Web画面へアクセス

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください。  

📖 [http://localhost:8000/tic-tac-toe/v3/match-request/](http://localhost:8000/tic-tac-toe/v3/match-request/)  
