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

以下のファイルを作成してほしい。  

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

{% block method_section1 %}
                    // フッターのボタンは除きました
{% endblock method_section1 %}
```

# Step 3. ビュー作成 - v_tic_tac_toe_v3.py ファイル

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
👉              └── v_tic_tac_toe_v3.py
```

```py
from django.http import Http404
from django.shortcuts import render, redirect


class MatchApplication():
    """対局申込ページ"""

    @staticmethod
    def render(request):
        """描画"""

        if request.method == "POST":
            # 送信後
            MatchApplication.on_sent(request)

            # `po_` は POST送信するパラメーター名の目印
            room_name = request.POST.get("po_room_name")
            my_piece = request.POST.get("po_my_piece")
            return redirect(f'/tic-tac-toe/v3/playing/{room_name}/?&mypiece={my_piece}')
            #                               ^ three
            #                 --------------------------------------------------------
            #                 1
            # 1. http://example.com:8000/tic-tac-toe/v3/playing/Elephant/?&mypiece=X
            #                           --------------------------------------------

        # 訪問後
        MatchApplication.on_visited(request)
        return render(request, "webapp1/tic-tac-toe/v2/match_application.html", {})
        #                                            ^ two
        #                       ---------------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
        #                            ---------------------------------------------

    @staticmethod
    def on_sent(request):
        """送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass

    @staticmethod
    def on_visited(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く
        pass


class Playing():
    """対局ページ"""

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        my_piece = request.GET.get("mypiece")
        if my_piece not in ['X', 'O']:
            raise Http404(f"My piece '{my_piece}' does not exists")

        Playing.on_update(request)

        # `dj_` は Djangoでレンダーするパラメーター名の目印
        context = {
            "dj_room_name": kw_room_name,
            "dj_my_piece": my_piece,
            "dj_path_of_playing": "/tic-tac-toe/v2/playing/",
            #                                    ^ two
        }
        return render(request, "webapp1/tic-tac-toe/v3/playing.html.txt", context)
        #                                            ^ three
        #                       ---------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/playing.html.txt
        #                            ---------------------------------------

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass
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
            │               └── playing.html.txt
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

    # 対局申込
    path('tic-tac-toe/v3/match-application/',
         #             ^
         # --------------------------------
         # 1
         v_tic_tac_toe_v3.MatchApplication.render),
    #                   ^
    #    ----------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/match-application/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. v_tic_tac_toe_v3.py ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3/playing/<str:kw_room_name>/',
         #             ^
         # -----------------------------------------
         # 1
         v_tic_tac_toe_v3.Playing.render),
    #                   ^
    #    -------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/playing/<部屋名>/` のような URL のパスの部分。
    #                              --------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. v_tic_tac_toe_v3.py ファイルの Playing クラスの render 静的メソッド
]
```

# Step 5. Web画面へアクセス

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください。  

📖 [http://localhost:8000/tic-tac-toe/v3/match-application/](http://localhost:8000/tic-tac-toe/v3/match-application/)  

# 次の記事

📖 [Djangoでチェックインを作ろう！](https://qiita.com/muzudho1/items/1ce542dd66929d7bce3f)  
