# 目的

Vuetify を自由自在に使えるよう、使用スキルを上げたい。  
Data table を作れば上がる。だから説明する。  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
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

# Step 1. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄vuetify-data-table1.html
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
            new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    headers: [
                        {
                            text: "Dessert (100g serving)",
                            align: "start",
                            sortable: false,
                            value: "name",
                        },
                        { text: "Calories", value: "calories" },
                        { text: "Fat (g)", value: "fat" },
                        { text: "Carbs (g)", value: "carbs" },
                        { text: "Protein (g)", value: "protein" },
                        { text: "Iron (%)", value: "iron" },
                    ],
                    desserts: [
                        {
                            name: "Frozen Yogurt",
                            calories: 159,
                            fat: 6.0,
                            carbs: 24,
                            protein: 4.0,
                            iron: "1%",
                        },
                        {
                            name: "Ice cream sandwich",
                            calories: 237,
                            fat: 9.0,
                            carbs: 37,
                            protein: 4.3,
                            iron: "1%",
                        },
                        {
                            name: "Eclair",
                            calories: 262,
                            fat: 16.0,
                            carbs: 23,
                            protein: 6.0,
                            iron: "7%",
                        },
                        {
                            name: "Cupcake",
                            calories: 305,
                            fat: 3.7,
                            carbs: 67,
                            protein: 4.3,
                            iron: "8%",
                        },
                        {
                            name: "Gingerbread",
                            calories: 356,
                            fat: 16.0,
                            carbs: 49,
                            protein: 3.9,
                            iron: "16%",
                        },
                        {
                            name: "Jelly bean",
                            calories: 375,
                            fat: 0.0,
                            carbs: 94,
                            protein: 0.0,
                            iron: "0%",
                        },
                        {
                            name: "Lollipop",
                            calories: 392,
                            fat: 0.2,
                            carbs: 98,
                            protein: 0,
                            iron: "2%",
                        },
                        {
                            name: "Honeycomb",
                            calories: 408,
                            fat: 3.2,
                            carbs: 87,
                            protein: 6.5,
                            iron: "45%",
                        },
                        {
                            name: "Donut",
                            calories: 452,
                            fat: 25.0,
                            carbs: 51,
                            protein: 4.9,
                            iron: "22%",
                        },
                        {
                            name: "KitKat",
                            calories: 518,
                            fat: 26.0,
                            carbs: 65,
                            protein: 7,
                            iron: "6%",
                        },
                    ],
                },
            });
        </script>
    </body>
</html>
```

👆 `<v-data-table>` の説明は 📖[Vuetify - Data tables - Usage](https://vuetifyjs.com/en/components/data-tables/#dense) のページにある。  

# Step 2. ビュー編集 - v_practice_of_vuetify.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄vuetify-data-table1.html
            └── 📂views
👉              └── v_practice_of_vuetify.py
```

```py
from django.http import HttpResponse
from django.template import loader


def readDataTable1(request, id=id):
    """Vuetify練習"""

    template = loader.get_template('practice/vuetify-data-table1.html')
    #                               ---------------------------------
    #                               1
    # 1. host1/webapp1/templates/practice/vuetify-data-table1.html を取ってきます。
    #                            ---------------------------------

    context = {
    }

    return HttpResponse(template.render(context, request))
```

# Step 3. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄vuetify-data-table1.html
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

    # Vuetify練習
    path('practice/vuetify-data-table1', v_practice_of_vuetify.readDataTable1,
         # ---------------------------   ------------------------------------
         # 1                             2
         name='readDataTable1'),
    #          --------------
    #          3
    # 1. `practice/vuetify-data-table1` というURLにマッチ
    # 2. v_practice_of_vuetify.py ファイルの readDataTable1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable1' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/practice/vuetify-data-table1](http://localhost:8000/practice/vuetify-data-table1)  

# 次の記事

📖 [DjangoでVuetifyのテキストフィールドのバリデーションの練習をしよう！](https://qiita.com/muzudho1/items/fd47e589cd3f9449fcbb)  
