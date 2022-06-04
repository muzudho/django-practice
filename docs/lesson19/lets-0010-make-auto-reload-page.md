# 目的

待っていると　対局が付くページがほしい  

いきなり作るのは難しいので、まず 5秒毎に時刻の表示を更新するページ から作る  

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
        │   │   ├── 📂tic-tac-toe
        │   │   │   ├── 📂v1
        │   │   │   └── 📂v2
        │   │   │       └── 📄<いろいろ>.js
        │   │   ├── 📂<いろいろ>-practice
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

# Step 2. 機能強化 - clock.js ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄clock.js
```

```js
/**
 *
 * @returns 現在時刻の文字列
 */
function getTimeStamp() {
    const weekStr = ["日", "月", "火", "水", "木", "金", "土"];

    // 現在時刻
    const now = new Date();

    const text = String.format(
        `{0}年 {1}月 {2}日 （{3}） {4}時 {5}分 {6}秒 {7}ミリ秒`,
        now.getFullYear(), // 年
        now.getMonth() + 1, // 月
        now.getDate(), // 日
        now.getHours(), // 時
        now.getMinutes(), // 分
        now.getSeconds(), // 秒
        now.getMilliseconds(), // ミリ秒
        weekStr[now.getDay()] // 曜日
    );

    console.log(`time stamp=[${text}]`);

    return text;
}
```

# Step 3. 機能強化 - waiting-for-match.js ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
                        ├── 📄clock.js
👉                      └── 📄waiting-for-match.js
```

```js
/**
 * @param {number} intervalMilliseconds
 */
function startReloadingAutomatically(intervalMilliseconds) {
    setInterval(() => {
        location.reload();
    }, intervalMilliseconds);
}
```

# Step 4. テンプレート編集 - waiting-for-match-v1.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           ├── 📄clock.js
            │           └── 📄waiting-for-match.js
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄waiting-for-match-v1.html
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
                    startReloadingAutomatically(5000);
                },
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印
                    vu_timeStamp: getTimeStamp(),
                },
            });
        </script>
    </body>
</html>
```

# Step 5. ビュー編集 - v_practice.py ファイル

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
            │           └── 📄waiting-for-match-v1.html
            └── 📂views
👉              └── 📄v_practice.py
```

```py
from django.shortcuts import render

# ...中略...

def render_waiting_for_match(request):
    """対局待合室"""

    context = {
    }

    return render(request, "webapp1/practice/waiting-for-match-v1.html", context)
    #                       ------------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/practice/waiting-for-match-v1.html
    #                            ------------------------------------------
```

# Step 6. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models_helper
            │   └── 📄mh_user.py
            ├── 📂static
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           ├── 📄clock.js
            │           └── 📄waiting-for-match.js
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄waiting-for-match-v1.html
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

    # 対局待合室
    path('practice/waiting-for-match/',
         # --------------------------
         # 1
         v_practice.render_waiting_for_match, name='practice_waitingForMatch'),
    #    -----------------------------------        ------------------------
    #    2                                          3
    #
    # 1. 例えば `http://example.com/waiting-for-match/` のような URL のパスの部分
    #                              -------------------
    # 2. v_practice.py ファイルの render_waiting_for_match メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_waitingForMatch' %} のような形でURLを取得するのに使える
]
```

# Step 7. Web画面へアクセス

📖 [http://localhost:8000/practice/waiting-for-match/](http://localhost:8000/practice/waiting-for-match/)  

# 次の記事

📖 [Djangoで自動リダイレクトするページを作ろう！](https://qiita.com/muzudho1/items/aea9be36422763f082e9)  
