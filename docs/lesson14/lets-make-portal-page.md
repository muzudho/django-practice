# 目的

スマホアプリを起動したときに出てくる "対局開始" ボタンが置いてある画面がほしい。  
オープニングデモとか 演出もりもりのタイトル画面とか要らない  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

参考にした元記事は 📖[DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

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
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   ├── 📂webapp1
        │   │   │   ├── 📂practice
        │   │   │   │   └── 📄vuetify-desserts.json
        │   │   │   └── 📂tic-tac-toe
        │   │   │       ├── 📂v1
        │   │   │       │   └── 📄<いろいろ>
        │   │   │       └── 📂v2
        │   │   │           └── 📄<いろいろ>.js
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
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           └── 📄<いろいろ>.py
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

# Step 2. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
👉                          └── 📄portal.html
```

👇レッスンの進み具合によって、埋め込んであるURLは 貼り替えてください  

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>〇×ゲーム</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <v-row class="my-2">
                            <h3>〇×ゲーム</h3>
                        </v-row>
                        <v-row class="my-2">
                            <v-btn :href="createGamePath()">すぐやる</v-btn>
                        </v-row>
                        {% if user.is_authenticated %}
                        <v-row class="my-2">
                            <v-btn :href="createLogoutPath()">ログアウト</v-btn>
                        </v-row>
                        {% else %}
                        <v-row class="my-2">
                            <v-btn :href="createLoginPath()">ログイン／会員登録</v-btn>
                        </v-row>
                        {% endif %}
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印

                    // URL は、レッスンの進み具合によって適宜、貼り替えてください
                    vu_pathOfMatchApplication: "{{ dj_pathOfMatchApplication }}",

                    // vu_pathOfSignin: "{{ dj_pathOfSignin }}",
                    vu_pathOfSignin: "{% url 'accounts_v1_login' %}",

                    vu_pathOfLogout: "{{ dj_pathOfLogout }}",
                },
                methods: {
                    createGamePath() {
                        let path = `${location.protocol}//${location.host}${this.vu_pathOfMatchApplication}`;
                        //          --------------------  ---------------]--------------------------------
                        //          1                     2               3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`game path=[${path}]`);
                        return path;
                    },
                    createLoginPath() {
                        let path = `${location.protocol}//${location.host}${this.vu_pathOfSignin}`;
                        console.log(`login path=[${path}]`);
                        return path;
                    },
                    createLogoutPath() {
                        let path = `${location.protocol}//${location.host}${this.vu_pathOfLogout}`;
                        console.log(`logout path=[${path}]`);
                        return path;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 3. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               └── 📄portal.html
            └── 📂views
                └── 📂tic_tac_toe
                    └── 📂v2o1
👉                      └── 📄resources.py
```

```py
"""〇×ゲームの練習２"""
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


class Portal():
    """ポータル"""

    _path_of_html = "webapp1/tic-tac-toe/v2/portal.html"
    #                ----------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/portal.html を取得
    #                            ----------------------------------

    _path_of_match_application = "/tic-tac-toe/v2/match-application/"
    #                             ----------------------------------
    #                             1
    # 1. http://example.com/tic-tac-toe/v2/match-application/
    #                      ----------------------------------

    _path_of_signin = "/tic-tac-toe/v2/login/"
    #                  ----------------------
    #                  1
    # 1. http://example.com/tic-tac-toe/v2/login/
    #                      ----------------------

    _path_of_signout = "/tic-tac-toe/v2/logout/"
    #                   -----------------------
    #                   1
    # 1. http://example.com/tic-tac-toe/v2/logout/
    #                      -----------------------

    @staticmethod
    def render(request):
        """描画"""
        return portal_render(request, Portal._path_of_html, Portal._path_of_match_application, Portal._path_of_signin, Portal._path_of_signout)


class LoggingIn():
    """ログイン中"""

    _path_of_playing = "/tic-tac-toe/v2/playing/{0}/?&mypiece={1}"
    #                                 ^ two
    #                   -----------------------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    _path_of_match_application = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                                  ^ two
    #                             ---------------------------------------------
    #                             1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    # 👇 このデコレーターを付けると、ログインしていないなら、 settings.py の LOGIN_URL で指定した URL に飛ばします。
    # インスタンスのメソッドや、クラスメソッドには付けられません。
    # 第一引数が self や clazz でないことに注意してください
    @login_required
    def render(request):
        """描画"""
        return logging_in_render(request, LoggingIn._path_of_playing, LoggingIn._path_of_match_application)


class LoggingOut():
    """ログアウト中"""

    @staticmethod
    def render(request):
        """描画"""
        return logging_out_render(request)


# 以下、関数


def portal_render(request, path_of_html, path_of_match_application, path_of_signinin, path_of_signout):
    """ポータル - 描画"""
    template = loader.get_template(path_of_html)

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,
        'dj_pathOfMatchApplication': path_of_match_application,
        'dj_pathOfSignin': path_of_signinin,
        'dj_pathOfLogout': path_of_signout,
    }
    return HttpResponse(template.render(context, request))


def logging_in_render(request, path_of_playing, path_of_match_application):
    """ログイン中 - 描画"""
    if request.method == "POST":
        # 送信後

        # `po_` は POST送信するパラメーター名の目印
        room_name = request.POST.get("po_room_name")
        my_piece = request.POST.get("po_my_piece")

        return redirect(path_of_playing.format(room_name, my_piece))

    # 訪問後
    return render(request, path_of_match_application, {})


def logging_out_render(request):
    """ログアウト中 - 描画"""

    logout(request)  # Django の認証機能のログアウトを使う

    return redirect('ticTacToeV2_portal')  # ホームに戻る
```

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               └── 📄portal.html
            ├── 📂views
            │   └── 📂tic_tac_toe
            │       └── 📂v2o1
            │           └── 📄resources.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views.tic_tac_toe.v2o1 import resources as tic_tac_toe_v2o1
#    ------- ----------------------        ---------    ----------------
#    1       2                             3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [
    # ...中略...

    # +----
    # | ポータル作成

    # 旧ポータル
    path('tic-tac-toe2/', tic_tac_toe_v2o1.Portal.render,
         # ------------   ------------------------------
         # 1              2
         name='ticTacToeV2_portal'),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe2/` のような URL のパスの部分
    #                              --------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの Portal クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2_portal' %} のような形でURLを取得するのに使える

    # ポータル
    path('tic-tac-toe/v2/', tic_tac_toe_v2o1.Portal.render,
         # --------------   ------------------------------
         # 1                2
         name='ticTacToeV2_portal'),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe/v2/` のような URL のパスの部分
    #                              ----------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの Portal クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2_portal' %} のような形でURLを取得するのに使える

    # ログイン
    path('tic-tac-toe/v2/login/', tic_tac_toe_v2o1.LoggingIn.render,
         # --------------------   ---------------------------------
         # 1                      2
         name='ticTacToeV2o1_loginUser'),
    #          -----------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe/v2/login/` のような URL のパスの部分
    #                              ----------------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの LoggingIn クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2o1_loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('tic-tac-toe/v2/logout/', tic_tac_toe_v2o1.LoggingOut.render,
         # ---------------------   ----------------------------------
         # 1                       2
         name='ticTacToeV2o1_logout'),
    #          --------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe/v2/logout/` のような URL のパスの部分
    #                              -----------------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの LoggingOut クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2o1_logout' %} のような形でURLを取得するのに使える

    # | ポータル作成
    # +----
]
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/tic-tac-toe/v2/](http://localhost:8000/tic-tac-toe/v2/)  

# 次の記事

📖 [Djangoでユーザーホームを作ろう！](https://qiita.com/muzudho1/items/37532c83235b7f9e60c9)  
