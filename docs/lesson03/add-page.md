---
title: DjangoでWebページを追加しよう！
tags: Django Docker
author: muzudho1
slide: false
---
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
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1
        │   ├── 📂templates
        │   │   └── 📂webapp1
        │   │       └── 📄<いろいろ>.html
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

# Step 1. HTMLファイルを置く

以下のファイルを作成してほしい。

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂templates
                └── 📂webapp1
👉                  └── 📄page1.html
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

# Step 2. ビュー作成 - v_page1.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📄page1.html
            └── 📂views
👉              └── 📄v_page1.py
```

```py
from django.http import HttpResponse
from django.template import loader


def page1(request):
    template = loader.get_template('webapp1/page1.html')
    context = {}
    return HttpResponse(template.render(context, request))
```

# Step 3. ルート編集 - urls.py

📄`host1/webapp1/urls.py` の、以下の該当箇所を追加してほしい。
以下のファイルを編集してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📄page1.html
            ├── 📂views
            │   └── 📄v_page1.py
👉          └── 📄urls.py
```

```py
# 冒頭
from django.urls import path

from webapp1.views import v_page1
#    ------- -----        -------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

# 追記
urlpatterns = [
    # ...中略...

    path('practice/page1', v_page1.page1, name='page1'),
    #     --------------   -------------        -----
    #     1                 2                    3
    # 1. URLの `practice/page1` というパスにマッチする
    # 2. v_page1.py ファイルの page1 メソッド
    # 3. HTMLテンプレートの中で {% url 'page1' %} のような形でURLを取得するのに使える
]
```

# Step 4. Webページにアクセスする

📖 [http://localhost:8000/practice/page1](http://localhost:8000/practice/page1)  

# 次の記事

📖 [Djangoでログインユーザー情報を表示しよう！](https://qiita.com/muzudho1/items/9f1ae4d0debc0b8aa4b1)  
