# 目的

Vuetify の テキストフィールド の バリデーション を練習したい  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Frontside | Vuetify                                   |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── <いろいろ>
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 画面作成 - HTMLファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄vuetify-text-field-validation1.html
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html>
    <head>
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" />
        <title>テキストフィールドのバリデーションの練習</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container fluid>
                        <h1>テキストフィールドのバリデーションの練習</h1>
                        <v-form method="POST">
                            {% csrf_token %}

                            <v-text-field v-model="roomName.value" :rules="roomName.rules" counter="25" hint="a-z, A-Z, _. Max 25 characters" label="Room name" name="room_name"></v-text-field>

                            <v-btn block elevation="2" type="submit"> Start Game </v-btn>
                        </v-form>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    roomName: {
                        value: "Elephant",
                        rules: [(v) => v.length <= 25 || "Max 25 characters"],
                        wordsRules: [(v) => v.trim().split(" ").length <= 5 || "Max 5 words"],
                    },
                    selectedMyPiece: "X",
                    pieces: ["X", "O"],
                },
            });
        </script>
    </body>
</html>
```

# Step 3. ビュー編集 - v_practice_of_vuetify.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄vuetify-text-field-validation1.html
            └── 📂views
👉              └── v_practice_of_vuetify.py
```

```py
from django.http import HttpResponse
from django.template import loader


def render_practice_text_field_validation1(request):
    """テキストフィールドのバリデーションの練習"""
    template = loader.get_template(
        'webapp1/practice/vuetify-text-field-validation1.html')
    #                     -----------------------------------
    #                     1
    # 1. host1/webapp1/templates/webapp1/practice/vuetify-text-field-validation1.html を取ってきます。
    #                            ----------------------------------------------------

    context = {
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
            │       └── 📂practice
            │           └── 📄vuetify-text-field-validation1.html
            ├── 📂views
            │   └── 📄v_practice_of_vuetify.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_practice_of_vuetify
#    ------- -----        ---------------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # Vuetifyのテキストフィールドのバリデーションの練習
    path('practice/vuetify-text-field-validation1', v_practice_of_vuetify.render_practice_text_field_validation1,
         # --------------------------------------   ------------------------------------------------------------
         # 1                                        2
         name='practice_text_field_validation1'),
    #          -------------------------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-text-field-validation1` のような URL のパスの部分
    #                              ---------------------------------------
    # 2. v_practice_of_vuetify.py ファイルの render_practice_text_field_validation1 メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_text_field_validation1' %} のような形でURLを取得するのに使える
]
```

# Step 5. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/practice/practice/vuetify-text-field-validation1](http://localhost:8000/practice/vuetify-text-field-validation1)  

# 次の記事

📖 [Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1)  
