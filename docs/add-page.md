---
title: DjangoでWebページを追加しよう！
tags: Django Docker
author: muzudho1
slide: false
---
# 目的

以下のようなページを追加する方法を説明する。  

```plain
http://<省略>.com/practice1/page1.html
                  -------- ------
                  1        2

                  1. 新規ディレクトリ
                  2. 新規ページ
```

# はじめに

前の記事：　📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📂templates
　│　　│    └── 📂webapp1
　│　　│        └── 📄<いろいろ>.html
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

# Step 1. HTMLファイルを置く

以下のファイルを作成してほしい。

📄`host1/webapp1/templates/webapp1/page1.html`

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

# Step 2. views.pyを編集する

📄`host1/webapp1/views.py` に、以下のメソッドを追加してほしい。

```py
# 冒頭
from django.http import HttpResponse
from django.template import loader

# 追加
def page1(request):
    template = loader.get_template('webapp1/page1.html')
    context = {}
    return HttpResponse(template.render(context, request))
```

# Step 3. urls.pyを編集する

📄`host1/webapp1/urls.py` の、以下の該当箇所を追加してほしい。

```py
# 冒頭
from django.urls import path
from . import views

# 追記
urlpatterns = [
    path('practice1/page1.html', views.page1, name='page1'),
    #     --------------------   -----------        -----
    #     1                      2                  3
    #
    # 1. URLのディレクトリ部分
    # 2. views.py の page1 メソッド
    # 3. この名前をキーにして 1. のディレクトリ部分を取得することができるらしい
]
```

# Step 4. Webページにアクセスする

📖 [http://localhost:8000/practice/page1](http://localhost:8000/practice/page1)  

# 次の記事

* 📖 `DjangoでWebページを追加しよう！` (このページ)
    * 📖 [Djangoでログインユーザー情報を表示しよう！](https://qiita.com/muzudho1/items/9f1ae4d0debc0b8aa4b1)
* 📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)  
