# 目的

Web ページで表示する内容を、JSON形式のテキストで渡したい  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key         | Value                                     |
| ----------- | ----------------------------------------- |
| OS          | Windows10                                 |
| Container   | Docker                                    |
| Auth        | allauth                                   |
| Frontend    | Vuetify                                   |
| Data format | JSON                                      |
| Editor      | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄vuetify-desserts.json
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂members
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

# Step 1. JSONファイルの再利用

以下の記事で掲載した JSON ファイルを再利用してほしい。  

* 📖 [Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1)
  * 📄`host1/webapp1/static/webapp1/practice/vuetify-desserts.json`

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂webapp1
                    └── 📂practice
👉                      └── 📄vuetify-desserts.json
```

👆 この JSON データは 📖[Vuetify - Data tables - Usage](https://vuetifyjs.com/en/components/data-tables/#dense) のページにある。  

# Step 2. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄vuetify-desserts.json
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄vuetify-json-textarea1.html
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
                        <form method="POST" action="data-table2o2">
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

# Step 3. HTMLファイルの再利用

以下の記事で掲載した HTML ファイルを再利用してほしい。  

* 📖 [Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1)
  * 📄`host1/webapp1/templates/practice/vuetify-data-table2.html`

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄vuetify-desserts.json
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
                        ├── 📄vuetify-json-textarea1.html
👉                      └── 📄vuetify-data-table2.html
```

# Step 4. ビュー編集 - v_practice_of_vuetify.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄vuetify-desserts.json
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           ├── 📄vuetify-json-textarea1.html
            │           └── 📄vuetify-data-table2.html
            └── 📂views
👉              └── 📄v_practice_of_vuetify.py
```

```py
import json
from django.http import HttpResponse
from django.template import loader


def readJsonTextarea1(request):
    """Vuetify練習"""
    template = loader.get_template(
        'webapp1/practice/vuetify-json-textarea1.html')
    #    --------------------------------------------
    #    1
    # 1. host1/webapp1/templates/webapp1/practice/vuetify-json-textarea1.html を取ってきます。
    #                            --------------------------------------------

    with open('webapp1/static/webapp1/practice/vuetify-desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2o2(request):
    """Vuetify練習"""
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template('webapp1/practice/vuetify-data-table2.html')
    #                               -----------------------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/vuetify-data-table2.html を取ってきます。
    #                            -----------------------------------------

    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))
```

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄vuetify-desserts.json
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           ├── 📄vuetify-json-textarea1.html
            │           └── 📄vuetify-data-table2.html
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
    path('practice/vuetify-json-textarea1', v_practice_of_vuetify.readJsonTextarea1,
         # ------------------------------   ---------------------------------------
         # 1                                2
         name='readJsonTextarea1'),
    #          -----------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-json-textarea1` のような URL のパスの部分
    #                              --------------------------------
    # 2. v_practice_of_vuetify.py ファイルの readJsonTextarea1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/vuetify-data-table2o2', v_practice_of_vuetify.readDataTable2o2,
         # -----------------------------   --------------------------------------
         # 1                               2
         name='readDataTable2o2'),
    #          ----------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-data-table2o2` のような URL のパスの部分
    #                              -------------------------------
    # 2. v_practice_of_vuetify.py ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2o2' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/practice/vuetify-json-textarea1](http://localhost:8000/practice/vuetify-json-textarea1)  

# 次の記事

📖 [DjangoのサーバーからデータをJSON形式のテキストで受信しよう！](https://qiita.com/muzudho1/items/d83760a6a4abadaf19c4)  
