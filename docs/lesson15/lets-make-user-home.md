# 目的

ログイン後に飛ばされるページを作りたい  

ただし、そのページには、まだ作っていないページへのリンクも先々貼っている  

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
        │   │   ├── 📄v_tic_tac_toe_v1.py
        │   │   ├── 📄v_tic_tac_toe_v2.py
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       │   └── 📄consumer.py
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

# Step 2. 画面作成 - home.html ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂home
                        └── 📂v1
👉                          └── 📄home.html
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
        <title>あなたのホーム</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <v-row class="my-2">
                            <h3>あなたのホーム</h3>
                        </v-row>
                        <v-row class="my-2">
                            <v-btn :href="createLobbyPath()">ロビー（待合室）へ移動する</v-btn>
                        </v-row>
                        <v-row class="my-2">
                            <v-btn :href="createTicTacToePath()">〇×ゲーム</v-btn>
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
                    vu_lobbyPath: "{{ dj_lobbyPath }}",
                    vu_ticTacToePath: "{{ dj_ticTacToePath }}",
                    vu_loginPath: "{{ dj_loginPath }}",
                    vu_logoutPath: "{{ dj_logoutPath }}",
                },
                methods: {
                    createLobbyPath() {
                        let url = `${location.protocol}//${location.host}${this.vu_lobbyPath}`;
                        //          --------------------  --------------]--------------------
                        //          1                     2              3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`game url=[${url}]`);
                        return url;
                    },
                    createTicTacToePath() {
                        let url = `${location.protocol}//${location.host}${this.vu_ticTacToePath}`;
                        console.log(`game url=[${url}]`);
                        return url;
                    },
                    createLoginPath() {
                        let url = `${location.protocol}//${location.host}${this.vu_loginPath}`;
                        console.log(`login url=[${url}]`);
                        return url;
                    },
                    createLogoutPath() {
                        let url = `${location.protocol}//${location.host}${this.vu_logoutPath}`;
                        console.log(`logout url=[${url}]`);
                        return url;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 3. ビュー編集 - v_home.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂home
            │           └── 📂v1
            │               └── 📄home.html
            └── 📂views
👉              └── 📄v_home.py
```

```py
from django.http import HttpResponse
from django.template import loader


def render_home(request):
    """ホーム"""
    template = loader.get_template('webapp1/home/v1/home.html')
    #                               -------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/home/v1/home.html を取得
    #                            -------------------------

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,

        'dj_lobbyPath': '/lobby/v1/',
        #                ----------
        #                1
        # 1. http://example.com/lobby/v1/
        #                      ----------

        'dj_ticTacToePath': '/tic-tac-toe/v2/match-application/',
        #                    ----------------------------------
        #                    1
        # 1. http://example.com/tic-tac-toe/v2/match-application/
        #                      ----------------------------------

        'dj_loginPath': '/accounts/v1/login/',
        #                -------------------
        #                1
        # 1. http://example.com/accounts/v1/login/
        #                      -------------------

        'dj_logoutPath': '/accounts/v1/logout/',
        #                 --------------------
        #                 1
        # 1. http://example.com/accounts/v1/logout/
        #                      --------------------
    }

    return HttpResponse(template.render(context, request))
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂home
            │           └── 📂v1
            │               └── 📄home.html
            ├── 📂views
            │   └── 📄v_home.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_home
#    ------- -----        ------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # ポータル
    path('home/v1/', v_home.render_home, name='homeV1_home'),
    #     --------   ------------------        -----------
    #     1          2                         3
    #
    # 1. URLの `home/v1/` というパスにマッチする
    # 2. v_home.py ファイルの render_home メソッド
    # 3. HTMLテンプレートの中で {% url 'homeV1_home' %} のような形でURLを取得するのに使える
]
```

# Step 5. 設定編集 - settings.py ファイル

以下のファイルを編集してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂home
            │           └── 📂v1
            │               └── 📄home.html
            ├── 📂views
            │   └── 📄v_home.py
👉          ├── 📄settings.py
            └── 📄urls.py
```

```py
# (Old) LOGIN_REDIRECT_URL = 'home'  # ログイン後に遷移するURLの指定
LOGIN_REDIRECT_URL = 'homeV1_home'  # ログイン後に遷移するURLの指定
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/home/v1/](http://localhost:8000/home/v1/)  

# 次の記事

📖 [Djangoでアクティブユーザーの一覧を作ろう！](https://qiita.com/muzudho1/items/bea77e8a69c5c805e1d7)  
