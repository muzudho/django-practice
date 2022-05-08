---
title: DjangoのWebページへJSON形式のテキストを渡そう！
tags: Django Vuetify JSON
author: muzudho1
slide: false
---
# 目的

JSON形式のテキストをサーバーへ渡して、その内容を Web ページで表示したい。
サーバーへデータを JSON形式で渡す Web ページの作成方法と、渡された JSON を Vuetify で利用する Web ページの作成方法を説明する。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                                                                      | Value                                                                                                                  |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込む方法を知っておく | 📖[Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1) |

この記事のアーキテクチャ:  

| Key         | Value                                     |
| ----------- | ----------------------------------------- |
| OS          | Windows10                                 |
| Container   | Docker                                    |
| Auth        | allauth                                   |
| Frontend    | Vuetify                                   |
| Data format | JSON                                      |
| Editor      | Visual Studio Code （以下 VSCode と表記） |

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📂static
　│　　│    └── 📄desserts.json
　│　　├── 📂templates
　│　　│    └── 📂vuetify2
　│　　│        ├── 📄data-table1.html
　│　　│        ├── 📄data-table2.html
　│　　│        └── 📄hello1.html
　│　　├── 📄models.py
　│　　├── 📄settings.py
　│　　├── 📄urls.py
　│　　├── 📄views.py
　│　　└── <いろいろ>
　├── 📄.env
　├── 🐳docker-compose.yml
　├── 🐳Dockerfile
　├── 📄manage.py
　└── <いろいろ>
```

# Step 1. JSONファイルの作成

（再掲）以下のファイルを作成してほしい。  

📄`host1/webapp1/static/desserts.json`:  

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

👆 以上のデータは 📖[Vuetify - Data tables - Usage](https://vuetifyjs.com/en/components/data-tables/#dense) のページにある。  

# Step 2. HTMLファイルの作成＜その１＞

以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/vuetify2/json-textarea1.html`:  

```html
<!DOCTYPE html>
<!-- See also: https://vuetifyjs.com/en/components/textareas/#counter -->
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
                    <v-container fluid>
                        <form method="POST" action="data-table2-b">
                            <!-- form要素の中に csrf_token を入れてください -->
                            {% csrf_token %}
                            <v-textarea counter name="textarea1" label="JSONを入力してください" :rules="rules" :value="value"></v-textarea>
                            <v-btn type="submit" class="mr-4">送信</v-btn>
                        </form>
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
                data: {
                    rules: [(v) => v.length <= 3000 || "Max 3000 characters"],
                    value: JSON.stringify(dessertsDoc, null, "    "),
                },
            });
        </script>
    </body>
</html>
```

# Step 3. HTMLファイルの作成＜その２＞

（再掲）以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/vuetify2/data-table2.html`:  

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

# Step 4. views.pyファイルの編集

📄`views.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/views.py`:  

```py
import json
from django.http import HttpResponse
from django.template import loader

# （追加）Vuetify練習
def readJsonTextarea1(request):
    template = loader.get_template('vuetify2/json-textarea1.html')

    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))

# （追加）Vuetify練習
def readDataTable2b(request):
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template('vuetify2/data-table2.html')
    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))
```

# Step 5. urls.pyファイルの編集

📄`urls.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/urls.py`:  

```py
from django.urls import path
from . import views

urlpatterns = [
    # （追加）Vuetify練習
    path('vuetify2/json-textarea1.html', views.readJsonTextarea1, name='readJsonTextarea1'),
    #     ----------------------------                                  -----------------
    #     1                                                             2
    # 1. `vuetify2/json-textarea1.html` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readJsonTextarea1' %} のような形でURLを取得するのに使える

    # （追加）Vuetify練習
    path('vuetify2/data-table2-b', views.readDataTable2b, name='readDataTable2b'),
    #     ----------------------                                ---------------
    #     1                                                     2
    # 1. `vuetify2/data-table2-b` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readDataTable2b' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/vuetify2/json-textarea1.html](http://localhost:8000/vuetify2/json-textarea1.html)  

# 次の記事

📖 [DjangoのサーバーからデータをJSON形式のテキストで受信しよう！](https://qiita.com/muzudho1/items/d83760a6a4abadaf19c4)  
