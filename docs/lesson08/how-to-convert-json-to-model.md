---
title: DjangoでデータをサーバーへJSON形式で渡して、記憶させよう！
tags: Django Docker Vuetify JSON
author: muzudho1
slide: false
---
# 目的

データをJSON形式で渡して、サーバーへ記憶させたい。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                                                              | Value                                                                                                                  |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| WebページへJSON形式のテキストを渡す方法を知っておく              | 📖[DjangoのWebページへJSON形式のテキストを渡そう！](https://qiita.com/muzudho1/items/c50859d9bde800d06a62)              |
| サーバーからデータをJSON形式のテキストで受信する方法を知っておく | 📖[DjangoのサーバーからデータをJSON形式のテキストで受信しよう！](https://qiita.com/muzudho1/items/d83760a6a4abadaf19c4) |

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
　│　　│        ├── 📄hello1.html
　│　　│        └── 📄json-textarea1.html
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

# Step 1. models.pyファイルの編集

JSONのデータを受け入れられる形をサーバー側で定義しておく必要がある。  
おおまかに言って以下のような形だ。  

モデルの表示名: `Dessert (100g serving)`

| キー名   | 表示名      | サイズ               | デフォルト | ブランク | Example    |
| -------- | ----------- | -------------------- | ---------- | -------- | ---------- |
| name     | Name        | 最大32文字程度で十分 |            | 不可     | "Lollipop" |
| calories | Calories    | 自然数3桁程度        | 0          | 可       | 392        |
| fat      | Fat (g)     | 0.0～100.0程度       | 0          | 可       | 0.2        |
| carbs    | Carbs (g)   | 自然数2桁程度        | 0          | 可       | 98         |
| protein  | Protein (g) | 0.0～10.0程度        | 0          | 可       | 0          |
| iron     | Iron (%)    | 最大4文字程度で十分  |            | v"2%"    |

以上から、以下のコードを記述してほしい。  
ファイルは既存だろうから、マージしてほしい。  

📄`host1/webapp1/models.py`:  

```py
from django.db import models

class Dessert(models.Model):

    name = models.CharField('Name', max_length=32)
    calories = models.IntegerField('Calories', blank=True, default=0)
    fat = models.FloatField('Fat (g)', blank=True, default=0)
    carbs = models.IntegerField('Carbs (g)', blank=True, default=0)
    protein = models.FloatField('Protein (g)', blank=True, default=0)
    iron = models.CharField('Iron (%)', max_length=4, blank=True)

    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return self.name
```

# Step 2. コマンド実行

```shell
cd host1

docker-compose run --rm web python3 manage.py makemigrations webapp1
#                                                            -------
#                                                            1
# 1. アプリケーション ディレクトリー名
```

以下のディレクトリーとファイルが生成される。  

```plaintext
📂host1
　└── 📂webapp1
　 　　└── 📂migrations
　 　　     ├── 📄__init__.py
　 　　     ├── ＜既存のいろいろなファイル＞
　 　　     └── 📄0002_dessert.py
```

👆 これらのファイルは マイグレーション ファイル と呼ぶらしい。  

# Step 3. コマンド実行＜その２＞

```shell
docker-compose run --rm web python manage.py migrate
```

👆 ここまでやって マイグレーション という作業が終わるらしい。  

# Step 4. admin.py を作成

以下のファイルを作成してほしい。既存ならマージしてほしい。  

📄`host1/webapp1/admin.py`:  

```py
from django.contrib import admin
from .models import Dessert # 追加

admin.site.register(Dessert) # 追加
```

👆 管理画面から Dessert オブジェクトを編集できるようにした。  

# Step 5. スーパーユーザーでWebの管理画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

画面左に

```plain
WEBAPP1
Desserts +Add
```

のように表示されていればOK。  
されていなければ、スーパーユーザーでログインし直してほしい。  

# Step 6. Dessert を３つほど追加してほしい

`Desserts +Add` の右側の `+Add` リンクをクリックしてほしい。  

```plaintext
Name:
      ----------------

Calories:
          ----

Fat (g):
         ----

Carbs (g):
           ----

Protein (g): 
             ----

Iron (%): 
          ----

                [Save and add another] [Save and continue editing] [SAVE]
```

👆入力フォームが出てくるから、３件ほど適当に追加してほしい。  
`[SAVE]` が追加ボタンのようだ。  

# Step 7. 登録した Dessert を確認してほしい

`Members +Add` の `Desserts` リンクをクリックすると、一覧画面が出てくる。  

# Step 8. JSONファイルの作成

既に JSON 形式のテキストファイルを持っているなら、それを手入力するのは避け、  
サーバーへ送信することでデータの入力が行われるようにしたい。  

以下のファイルを作成してほしい。  

📄`host1/webapp1/static/desserts-placeholder.json`:  

```json
{
    "name": "",
    "calories": 0,
    "fat": 0,
    "carbs": 0,
    "protein": 0,
    "iron": "0%"
}
```

# Step 9. HTMLファイルの作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/vuetify2/json-textarea2.html`:  

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
                        <form method="POST" action="data-table2-c">
                            <!--                    =============
                                                    1
                            1. 宛先を間違えないように
                            -->
                            {% csrf_token %}
                            <!--
                               ==========
                               2
                            2. form要素の中に csrf_token を入れてください
                            -->
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

# Step 10. views.pyファイルの編集

📄`views.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/views.py`:  

```py
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Dessert # 追加

# （追加）
def readJsonTextarea2(request):
    template = loader.get_template('vuetify2/json-textarea2.html')

    with open('webapp1/static/desserts-placeholder.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))

# （追加）
def readDataTable2c(request):
    form1Textarea1 = request.POST["textarea1"]
    doc = json.parse(form1Textarea1) # Dessert

    record = Dessert(
        name=doc["name"],
        calories=doc["calories"],
        fat=doc["fat"],
        carbs=doc["carbs"],
        protein=doc["protein"],
        iron=doc["iron"])
    record.save()

    doc2 = {
        'result': "Success"
    }
    return JsonResponse(doc2)
```

# Step 11. urls.pyファイルの編集

📄`urls.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/urls.py`:  

```py
from django.urls import path
from . import views

urlpatterns = [
    # （追加）
    path('vuetify2/json-textarea2.html', views.readJsonTextarea2, name='readJsonTextarea2'),
    #     ----------------------------                                  -----------------
    #     1                                                             2
    # 1. `vuetify2/json-textarea2.html` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readJsonTextarea2' %} のような形でURLを取得するのに使える

    # （追加）
    path('vuetify2/data-table2-c', views.readDataTable2c, name='readDataTable2c'),
    #     ----------------------                                ---------------
    #     1                                                     2
    # 1. `vuetify2/data-table2-c` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readDataTable2c' %} のような形でURLを取得するのに使える
]
```

# Step 12. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/vuetify2/json-textarea2.html](http://localhost:8000/vuetify2/json-textarea2.html)  

