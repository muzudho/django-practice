# 目的

サーバーからデータをJSON形式で受信したい。  

# はじめに

前提知識:  

| Key                                                 | Value                                                                                                     |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| WebページへJSON形式のテキストを渡す方法を知っておく | 📖[DjangoのWebページへJSON形式のテキストを渡そう！](https://qiita.com/muzudho1/items/c50859d9bde800d06a62) |

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

# Step 1. JSONファイルの再利用

以下の記事で掲載した JSON ファイルを再利用してほしい。  

* 📖 [Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1)
  * 📄`host1/webapp1/static/vuetify-practice/desserts.json`:

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂vuetify-practice
👉                  └── 📄desserts.json
```

👆 この JSON データは 📖[Vuetify - Data tables - Usage](https://vuetifyjs.com/en/components/data-tables/#dense) のページにある。  

# Step 2. ビュー編集 - v_json_practice.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂vuetify-practice
            │       └── 📄desserts.json
            └── 📂views
👉              └── 📄v_json_practice.py
```

```py
import json
from django.http import JsonResponse # 追加


def readJsonResponse1(request):
    """JSONでの応答練習"""
    with open('webapp1/static/vuetify-practice/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    return JsonResponse(doc)
```

# Step 3. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂vuetify-practice
            │       └── 📄desserts.json
            ├── 📂views
            │   └── 📄v_json_practice.py
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

    # Vuetify練習
    path('json-practice/response1',
         # ----------------------
         # 1
         v_json_practice.readJsonResponse1, name='readJsonResponse1'),
    #    ---------------------------------        -----------------
    #    2                                        3
    # 1. URLの `practice1/json-response1` というパスにマッチする
    # 2. v_json_practice.py ファイルの readJsonResponse1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonResponse1' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/json-practice/response1](http://localhost:8000/json-practice/response1)  

# 次の記事

📖 [DjangoでデータをサーバーへJSON形式で渡して、記憶させよう！](https://qiita.com/muzudho1/items/ed0ea262aaa327a2d12b)  
