# 目的

待っていると　対局が付くページがほしい  

いきなり作るのは難しいので、まず サーバーサイドで時計を見て  
0分、5分、10分、... のような 分が 5 で割り切れるタイミングで  
クライアントのページをリダイレクトする  

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

# Step 2. 機能強化 - waiting-for-match.js ファイル

以下の既存のファイルへマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄waiting-for-match.js
```

```js
/**
 * 内部で使用する変数
 *
 * * vue1
 *
 * @param {number} intervalMilliseconds
 */
function startReloadingAutomatically_v2(intervalMilliseconds) {
    setInterval(() => {
        // setInterval に渡すラムダ関数の中で this を使うのは、正しく理解する知識が難しいので避けます
        const redirectUrl = vue1.createRedirectUrl();

        if (redirectUrl) {
            // リダイレクトします
            window.location.href = redirectUrl;
        } else {
            // JavaScript では、空文字列は 偽
            // リロードします
            location.reload();
        }
    }, intervalMilliseconds);
}
```

# Step 3. テンプレート編集 - waiting-for-match-v2.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄waiting-for-match.js
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄waiting-for-match-v2.html
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
        <title>対局待合室</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <!-- v-app-bar に app プロパティを指定しないなら、背景画像を付けてほしい -->
                <v-app-bar app dense elevation="4">
                    <v-app-bar-nav-icon></v-app-bar-nav-icon>
                    <v-toolbar-title>ゲーム対局サーバー</v-toolbar-title>
                </v-app-bar>
                <v-main>
                    <v-container>
                        <h3>対局待合室</h3>
                        <!-- ここに時計 -->
                        {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %}
                        <!-- -->
                        {% verbatim %} {{vu_timeStamp}} {% endverbatim %}
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <!--
            host1/static/webapp1/practice/clock.js
                        ==========================
        -->
        <script src="{% static 'webapp1/practice/clock.js' %}"></script>
        <script src="{% static 'webapp1/practice/waiting-for-match.js' %}"></script>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                // page loaded
                mounted: () => {
                    // ここで Vue の準備完了後の処理ができる。
                    // ただし、まだ this は初期化されてない

                    // 5秒毎にリロード
                    startReloadingAutomatically_v2(5000);
                    //                         ---
                },
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印
                    // "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
                    vu_timeStamp: getTimeStamp(),
                    vu_redirectPath: "{{ dj_redirect_path|escapejs }}",
                },
                methods: {
                    /**
                     * vue1.createRedirectUrl() のように使えます
                     */
                    createRedirectUrl() {
                        if (!this.vu_redirectPath) {
                            // JavaScript では、空文字列を not すると 真
                            // リダイレクトしたくないときは空文字列を送る、という取り決めをしておきます
                            return "";
                        }

                        let url = `${location.protocol}//${location.host}${this.vu_redirectPath}`;
                        //         --------------------  ---------------]-----------------------
                        //         1                     2               3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`redirect url=[${url}]`);
                        return url;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 4. ビュー編集 - v_practice.py ファイル

以下のファイルを無ければ新規作成、有れば編集してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           ├── 📄clock.js
            │           └── 📄waiting-for-match.js
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄waiting-for-match-v2.html
            └── 📂views
👉              └── 📄v_practice.py
```

```py
import datetime
from django.shortcuts import render

# ...中略...

def render_waiting_for_match_v2(request):
    """対局待合室"""

    # 現在日時
    dt_now = datetime.datetime.now()

    # 今何分？
    dt_minute = dt_now.minute

    # 5 で割り切れる分なら、リダイレクト
    if dt_minute % 5 == 0:
        redirect_path = "/tic-tac-toe/v2/"
    else:
        # リダイレクトしたくないときは空文字列を送る、と取り決めておきます
        redirect_path = ""

    context = {
        # FIXME 相対パス。 URL を urls.py で変更したいとき、反映されないがどうするか？
        "dj_redirect_path": redirect_path,
    }

    return render(request, "webapp1/practice/waiting-for-match-v2.html", context)
    #                       ------------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/practice/waiting-for-match-v2.html
    #                            ------------------------------------------
```

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models_helper
            │   └── 📄mh_user.py
            ├── 📂static
        │   │   ├── 📂allauth-customized
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           ├── 📄clock.js
            │           └── 📄waiting-for-match.js
            ├── 📂templates
        │   │   ├── 📂allauth-customized
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄waiting-for-match-v2.html
            ├── 📂views
            │   └── 📄v_practice.py
👉          └── 📄urls.py
```

```py
from webapp1.views import v_practice
#    ------- -----        ----------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # 対局待合室 v2
    path('practice/waiting-for-match/v2/',
         # -----------------------------
         # 1
         v_practice.render_waiting_for_match_v2, name='practice_waitingForMatchV2'),
    #    --------------------------------------        --------------------------
    #    2                                             3
    #
    # 1. 例えば `http://example.com/waiting-for-match/v2/` のような URL のパスの部分
    #                              ----------------------
    # 2. v_practice.py ファイルの render_waiting_for_match_v2 メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_waitingForMatchV2' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/practice/waiting-for-match/v2/](http://localhost:8000/practice/waiting-for-match/v2/)  

# 次の記事

📖 [Djangoの〇×ゲームのPlayAgainボタンを外そう！](https://qiita.com/muzudho1/items/d4bfde69c1656616f8ce)  
