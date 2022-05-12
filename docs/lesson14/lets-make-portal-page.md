# 目的

スマホアプリを起動したときに出てくる "対局開始" ボタンが置いてある画面がほしい。  
オープニングデモとか 演出もりもりのタイトル画面とか要らない。  

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
        │   │   ├── 📂tic-tac-toe1
        │   │   │   └── 📄<いろいろ>
        │   │   ├── 📂tic-tac-toe2
        │   │   │    ├── 📄connection.js
        │   │   │    ├── 📄engine.js
        │   │   │    ├── 📄game.js
        │   │   │    ├── 📄judge.js
        │   │   │    ├── 📄protocol_main.js
        │   │   │    └── 📄protocol_messages.js
        │   │   ├── 📂vuetify-practice
        │   │   │   └── 📄desserts.json
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂tic-tac-toe1
        │   │   │   └── 📄<いろいろ>
        │   │   ├── 📂tic-tac-toe2
        │   │   │   ├── 📄index.html
        │   │   │   └── 📄game.html
        │   │   └── 📂<いろいろ>-practice
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂tic_tac_toe1
        │   │   └── 📄consumer1.py
        │   ├── 📂tic-tac-toe2
        │   │   ├── consumer1.py
        │   │   └── protocol.py
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websock1
        │   │   ├── 📄consumer1.py
        │   │   └── 📄consumer2.py
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
                └── 📂portal
👉                  └── 📄portal1.html
```

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
                        <v-row class="my-2">
                            <v-btn :href="createLoginPath()">ログイン／会員登録</v-btn>
                        </v-row>
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
                    // "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
                    // "vu_" は 「vue1.dataのメンバー」 の目印
                    vu_gamePath: "{{ dj_gamePath }}",
                    vu_loginPath: "{{ dj_loginPath }}",
                    vu_logoutPath: "{{ dj_logoutPath }}",
                },
                methods: {
                    createGamePath() {
                        return `${this.vu_gamePath}`;
                    },
                    createLoginPath() {
                        return `${this.vu_loginPath}`;
                    },
                    createLogoutPath() {
                        return `${this.vu_logoutPath}`;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 3. ビュー編集 - v_portal.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂portal
            │       └── 📄portal1.html
            └── 📂views
👉              └── 📄v_portal.py
```

```py
from django.http import HttpResponse
from django.template import loader


def visitPortal1(request):
    """ポータル１"""
    template = loader.get_template('portal/portal1.html')
    #                               -------------------
    #                               1
    # 1. host1/webapp1/templates/portal/portal1.html を取得
    #                            -------------------
    context = {
        'dj_gamePath': 'tic-tac-toe2/',
        #               -------------
        #               1
        # 1. http://example.com/tic-tac-toe2/
        #                       -------------
        'dj_loginPath': 'login/tic-tac-toe2',
        #                ------------------
        #                1
        # 1. http://example.com/login/tic-tac-toe2
        #                       ------------------
        'dj_logoutPath': 'logout/tic-tac-toe2',
        #                 -------------------
        #                 1
        # 1. http://example.com/logout/tic-tac-toe2
        #                       -------------------
    }
    return HttpResponse(template.render(context, request))
```

# Step 4. ビュー編集 - v_tic_tac_toe2o1.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂portal
            │       └── 📄portal1.html
            └── 📂views
                ├── 📄v_portal.py
👉              └── 📄v_tic_tac_toe2o1.py
```

```py
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required  # 👈 このデコレーターを付けると、ログインしていないなら、認証ページに飛ばします
def loginUser(request):
    """〇×ゲームの練習２"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe2/{room_name}/?&mypiece={myPiece}')
        #                             ^
    return render(request, "tic-tac-toe2/index.html", {})
    #                                  ^


def logoutUser(request):
    """ログアウト"""
    logout(request)
    return redirect('visitPortal1')
```

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂portal
            │       └── 📄portal1.html
            ├── 📂views
            │   └── 📄v_portal.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_portal
#    ------- -----        --------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

from webapp1.views import v_tic_tac_toe2o1
#    ------- -----        ----------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # ポータル１
    path('portal1', v_portal.visitPortal1, name='visitPortal1'),
    #     -------   ---------------------        ------------
    #     1         2                            3
    # 1. URLの `portal1` というパスにマッチする
    # 2. v_portal.py ファイルの visitPortal1 メソッド
    # 3. HTMLテンプレートの中で {% url 'visitPortal1' %} のような形でURLを取得するのに使える

    # ログイン
    path('login/tic-tac-toe2', v_tic_tac_toe2o1.loginUser,
         # -----------------   --------------------------
         # 1                    2
         name='ticTacToe2o1_loginUser'),
    #          ----------------------
    #          3
    # 1. URLの `login/tic-tac-toe2` というパスにマッチする
    # 2. v_tic_tac_toe2o1.py ファイルの loginUser メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToe2o1_loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('logout/tic-tac-toe2', v_tic_tac_toe2o1.logoutUser,
         # ------------------   ---------------------------
         # 1                    2
         name='ticTacToe2o1_logoutUser'),
    #          -----------------------
    #          3
    # 1. URLの `logout/tic-tac-toe2` というパスにマッチする
    # 2. v_tic_tac_toe2o1.py ファイルの logoutUser メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToe2o1_logoutUser' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/portal1](http://localhost:8000/portal1)  