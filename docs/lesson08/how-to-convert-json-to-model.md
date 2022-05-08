# 目的

データをJSON形式で渡して、サーバーへ記憶させたい。  

# はじめに

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

この記事は Lesson01 から続いていて、順にやってこないと ソースが足りず実行できないので注意されたい。  

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📂static
　│　　│    └── 📄desserts.json
　│　　├── 📂templates
　│　　│    └── 📂vuetify-practice
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

# Step 1. モデル編集 - m_dessert.py ファイル

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

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models
👉              └── 📄m_dessert.py
```

```py
# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models


class Dessert(models.Model):
    """デザート"""

    # プロパティの仕様を決める感じで
    name = models.CharField('Name', max_length=32)
    calories = models.IntegerField('Calories', blank=True, default=0)
    fat = models.FloatField('Fat (g)', blank=True, default=0)
    carbs = models.IntegerField('Carbs (g)', blank=True, default=0)
    protein = models.FloatField('Protein (g)', blank=True, default=0)
    iron = models.CharField('Iron (%)', max_length=4, blank=True)

    # このオブジェクトを文字列にしたとき返るもの
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
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
👉          ├── 📂migrations
👉          │   ├── 📄__init__.py
            │   ├── ＜既存のいろいろなファイル＞
👉          │   └── 📄0002_dessert.py
            └── 📂models
                └── 📄m_dessert.py
```

👆 これらのファイルは マイグレーション ファイル と呼ぶらしい。  

# Step 3. コマンド実行＜その２＞

```shell
docker-compose run --rm web python manage.py migrate
```

👆 ここまでやって マイグレーション という作業が終わるらしい。  

# Step 4. 管理画面更新 - admin.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄__init__.py
            │   ├── ＜既存のいろいろなファイル＞
            │   └── 📄0002_dessert.py
            ├── 📂models
            │   └── 📄m_dessert.py
👉          └── 📄admin.py
```

```py
from django.contrib import admin
from .models.m_dessert import Dessert

# Register your models here.
admin.site.register(Dessert)
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

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄__init__.py
            │   ├── ＜既存のいろいろなファイル＞
            │   └── 📄0002_dessert.py
            ├── 📂models
            │   └── 📄m_dessert.py
            ├── 📂static
            │   └── 📂json-practice
👉          │       └── 📄desserts-placeholder.json
            └── 📄admin.py
```

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

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄__init__.py
            │   ├── ＜既存のいろいろなファイル＞
            │   └── 📄0002_dessert.py
            ├── 📂models
            │   └── 📄m_dessert.py
            ├── 📂static
            │   └── 📂json-practice
            │       └── 📄desserts-placeholder.json
            ├── 📂templates
            │   └── 📂json-practice
👉          │       └── 📄json-textarea2.html
            └── 📄admin.py
```

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
                        <form method="POST" action="data-table2o3">
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

# Step 10. ビュー編集 - v_json_practice.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄__init__.py
            │   ├── ＜既存のいろいろなファイル＞
            │   └── 📄0002_dessert.py
            ├── 📂models
            │   └── 📄m_dessert.py
            ├── 📂static
            │   └── 📂json-practice
            │       └── 📄desserts-placeholder.json
            ├── 📂templates
            │   └── 📂json-practice
            │       └── 📄json-textarea2.html
            ├── 📂views
👉          │   └── 📄v_json_practice.py
            └── 📄admin.py
```

```py
import json
from django.http import HttpResponse
from django.template import loader

from webapp1.models.m_dessert import Dessert
#    ------- ------ ---------        -------
#    1       2      3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def readJsonTextarea2(request):
    """JSONでの応答練習"""
    template = loader.get_template('json-practice/json-textarea2.html')
    #                               ---------------------------------
    #                               1
    # 1. host1/webapp1/templates/json-practice/json-textarea2.html を取ってきます。
    #                            ---------------------------------

    with open('webapp1/static/json-practice/desserts-placeholder.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2o3(request):
    """JSONでの応答練習"""
    form1Textarea1 = request.POST["textarea1"]
    doc = json.loads(form1Textarea1)  # Dessert

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

# Step 11. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄__init__.py
            │   ├── ＜既存のいろいろなファイル＞
            │   └── 📄0002_dessert.py
            ├── 📂models
            │   └── 📄m_dessert.py
            ├── 📂static
            │   └── 📂json-practice
            │       └── 📄desserts-placeholder.json
            ├── 📂templates
            │   └── 📂json-practice
            │       └── 📄json-textarea2.html
            ├── 📂views
            │   └── 📄v_json_practice.py
            ├── 📄admin.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_json_practice
#    ------- -----        ---------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # JSONでの応答練習
    path('json-practice/textarea2',
         # ----------------------
         # 1
         v_json_practice.readJsonTextarea2, name='readJsonTextarea2'),
    #    ---------------------------------        -----------------
    #    2                                        3
    # 1. URLの `json-practice/textarea2` というパスにマッチする
    # 2. v_json_practice.py ファイルの readJsonTextarea2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea2' %} のような形でURLを取得するのに使える

    # JSONでの応答練習
    path('json-practice/data-table2o3',
         # --------------------------
         # 1
         v_json_practice.readDataTable2o3, name='readDataTable2o3'),
    #    --------------------------------        ----------------
    #    2                                       3
    # 1. URLの `json-practice/data-table2o3` というパスにマッチする
    # 2. v_json_practice.py ファイルの readDataTable2o3 メソッド
    # 2. HTMLテンプレートの中で {% url 'readDataTable2o3' %} のような形でURLを取得するのに使える
]
```

# Step 12. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/json-practice/textarea2](http://localhost:8000/json-practice/textarea2)  

# 次の記事

📖 [ソケットを使おう！](https://qiita.com/muzudho1/items/7a6501f7dbafbaa9b96c)  
