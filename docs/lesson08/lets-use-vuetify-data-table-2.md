# 目的

Vuetify に JSON形式でデータを渡したい。  
HTML の中の JavaScript に JSON を動的に埋め込もう。  

# はじめに

前提知識:  

| Key                                       | Value                                                                                           |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------- |
| VuetifyのData tableを使う方法を知っておく | 📖[DjangoでVuetifyのData tableを使おう！](https://qiita.com/muzudho1/items/2b01d3acce5ec1b5770b) |

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
| Frontside | Vuetify                                   |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

この記事は Lesson01 から続いていて、順にやってこないと ソースが足りず実行できないので注意されたい。  

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

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
        │   │   └── 📂vuetify-practice
        │   │       └── 📄<いろいろ>.html
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

# Step 1. JSONファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂vuetify-practice
👉                  └── 📄desserts.json
```

```json
{
    "headers": [
        {
            "text": "Dessert (100g serving)",
            "align": "start",
            "sortable": false,
            "value": "name"
        },
        { "text": "Calories", "value": "calories" },
        { "text": "Fat (g)", "value": "fat" },
        { "text": "Carbs (g)", "value": "carbs" },
        { "text": "Protein (g)", "value": "protein" },
        { "text": "Iron (%)", "value": "iron" }
    ],
    "desserts": [
        {
            "name": "Frozen Yogurt",
            "calories": 159,
            "fat": 6.0,
            "carbs": 24,
            "protein": 4.0,
            "iron": "1%"
        },
        {
            "name": "Ice cream sandwich",
            "calories": 237,
            "fat": 9.0,
            "carbs": 37,
            "protein": 4.3,
            "iron": "1%"
        },
        {
            "name": "Eclair",
            "calories": 262,
            "fat": 16.0,
            "carbs": 23,
            "protein": 6.0,
            "iron": "7%"
        },
        {
            "name": "Cupcake",
            "calories": 305,
            "fat": 3.7,
            "carbs": 67,
            "protein": 4.3,
            "iron": "8%"
        },
        {
            "name": "Gingerbread",
            "calories": 356,
            "fat": 16.0,
            "carbs": 49,
            "protein": 3.9,
            "iron": "16%"
        },
        {
            "name": "Jelly bean",
            "calories": 375,
            "fat": 0.0,
            "carbs": 94,
            "protein": 0.0,
            "iron": "0%"
        },
        {
            "name": "Lollipop",
            "calories": 392,
            "fat": 0.2,
            "carbs": 98,
            "protein": 0,
            "iron": "2%"
        },
        {
            "name": "Honeycomb",
            "calories": 408,
            "fat": 3.2,
            "carbs": 87,
            "protein": 6.5,
            "iron": "45%"
        },
        {
            "name": "Donut",
            "calories": 452,
            "fat": 25.0,
            "carbs": 51,
            "protein": 4.9,
            "iron": "22%"
        },
        {
            "name": "KitKat",
            "calories": 518,
            "fat": 26.0,
            "carbs": 65,
            "protein": 7,
            "iron": "6%"
        }
    ]
}
```

# Step 2. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂vuetify-practice
            │       └── 📄desserts.json
            └── 📂templates
                └── 📂vuetify-practice
👉                  └── 📄data-table2.html
```

```html
<!DOCTYPE html>
<!-- See also: https://vuetifyjs.com/en/components/data-tables/#dense -->
<html>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" />
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <v-data-table :headers="headers" :items="desserts" :items-per-page="5" class="elevation-1"></v-data-table>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            var dessertsDoc = JSON.parse("{{ dessertsJson|escapejs }}");

            new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: dessertsDoc,
            });
        </script>
    </body>
</html>
```

# Step 3. ビュー編集 - v_vuetify_practice.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂vuetify-practice
            │       └── 📄desserts.json
            ├── 📂templates
            │   └── 📂vuetify-practice
            │       └── data-table2.html
            └── 📂views
👉              └── 📄v_vuetify_practice.py
```

```py
import json  # 追加
from django.http import HttpResponse
from django.template import loader


def readDataTable2(request):
    """Vuetify練習"""
    template = loader.get_template('vuetify-practice/data-table2.html')
    #                               ---------------------------------
    #                               1
    # 1. host1/webapp1/templates/vuetify-practice/data-table2.html を取ってきます。
    #                            ---------------------------------

    with open('webapp1/static/vuetify-practice/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂vuetify-practice
            │       └── 📄desserts.json
            ├── 📂templates
            │   └── 📂vuetify-practice
            │       └── 📄data-table2.html
            ├── 📂views
            │   └── 📄v_vuetify_practice.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_vuetify_practice
#    ------- -----        ------------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # Vuetify練習
    path('vuetify-practice/data-table2.html', v_vuetify_practice.readDataTable2,
         # --------------------------------   ---------------------------------
         # 1                                  2
         name='readDataTable2'),
    #          --------------
    #          3
    # 1. URLの `vuetify-practice/data-table2` というパスにマッチする
    # 2. v_vuetify_practice.py ファイルの readDataTable2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2' %} のような形でURLを取得するのに使える
]
```

# Step 5. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/vuetify-practice/data-table2](http://localhost:8000/vuetify-practice/data-table2)  

# 次の記事

📖 [DjangoのWebページへJSON形式のテキストを渡そう！](https://qiita.com/muzudho1/items/c50859d9bde800d06a62)  

# 参考にした記事

* JSONをビューからテンプレートへ渡す方法
    * 📖 [Django: passing JSON from view to template](https://stackoverflow.com/questions/31151229/django-passing-json-from-view-to-template)
* Vuetifyのサンプルプログラム
    * 📖 [Vuetify - Data tables - Dense](https://vuetifyjs.com/en/components/data-tables/#dense)