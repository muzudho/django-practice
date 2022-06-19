# 目的

Webサイトのページを追加したい。  
以下のようなURLで表示させる。  

```plain
http://<省略>.com/practice/page1
------]---------]---------------
1      2         3

1. プロトコル
2. ホスト
3. パス
```

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
    └── 📂host1                   # あなたの開発用ディレクトリー。任意の名前
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂static
        │   │   └── 📂allauth-customized
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   ├── 📂views
        │   │   └── v_accounts_v1.py
        │   ├── 📄__init__.py
        │   └── 📄urls.py
        ├── 📄.env
        ├── 📄asgi.py
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        ├── 📄urls.py
        └── 📄wsgi.py
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 画面作成 - page1.html ファイル

以下のファイルを作成してほしい。

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂templates
                └── 📂webapp1
                    └── 📂practice
👉                      └── 📄page1.html
```

```html
<html>
    <head>
        <title>ページ１</title>
    </head>
    <body>
        テストだよ
    </body>
</html>
```

# Step 3. ビュー作成 - pages.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄page1.html
            └── 📂views
                └── 📂practice
👉                  └── 📄pages.py
```

```py
from django.http import HttpResponse
from django.template import loader


def render_page1(request):
    template = loader.get_template('webapp1/practice/page1.html')
    #                               ---------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/page1.html を取得
    #                            ---------------------------

    context = {}
    return HttpResponse(template.render(context, request))
```

# Step 4. ルート編集 - urls.py

📄`host1/webapp1/urls.py` の、以下の該当箇所を追加してほしい。
以下のファイルを編集してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂templates
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄page1.html
        │   ├── 📂views
        │   │   └── 📂practice
        │   │       └── 📄pages.py
👉      │   └── 📄urls.py                       # こちら
❌      └── 📄urls.py                           # これではない
```

```py
# 冒頭
from django.urls import path

from webapp1.views.practice import pages as practice_pages
#    ------- --------------        -----    --------------
#    1       2                     3        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

# 追記
urlpatterns = [
    # ...中略...

    path('practice/page1', practice_pages.render_page1, name='page1'),
    #     --------------   ---------------------------        -----
    #     1                2                                  3
    # 1. URLの `practice/page1` というパスにマッチする
    # 2. practice_pages (別名)ファイルの render_page1 メソッド
    # 3. HTMLテンプレートの中で {% url 'page1' %} のような形でURLを取得するのに使える
]
```

# Step 5. Webページにアクセスする

📖 [http://localhost:8000/practice/page1](http://localhost:8000/practice/page1)  

# 次の記事

📖 [DjangoのHTMLのボイラープレートを減らすテンプレートを使おう！](https://qiita.com/muzudho1/items/7dcfc068e0bec009d371)  
