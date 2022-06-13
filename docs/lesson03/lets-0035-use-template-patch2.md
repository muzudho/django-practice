# 目的

パッチを当てるようにテンプレートを改修したい  

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
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
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

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 画面作成 - page2_patch2.html.txt ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂templates
                └── 📂webapp1
                    └── 📂practice
👉                      └── 📄page2_patch2.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "practice/page2_patch1.html.txt" %}
<!-- -->
{#          ------------------------------
            1
1. host1/webapp1/templates/webapp1/practice/page2_patch1.html.txt
                                   ------------------------------
#}

<!-- -->
{% block section2o1 %}
<td>1</td>
<td>松</td>
<td>竹</td>
<td>梅</td>
{% endblock section2o1 %}
```

# Step 3. ビュー作成 - pages.py ファイル

以下の既存のファイルに、ソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄page2_patch2.html.txt
            └── 📂views
                └── 📂practice
👉                  └── 📄pages.py
```

```py
from django.http import HttpResponse
from django.template import loader


# ...中略...


def render_page2_patch2(request):
    """ページ２　パッチ２"""
    template = loader.get_template('webapp1/practice/page2_patch2.html.txt')
    #                               --------------------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/page2_patch2.html.txt を取得
    #                            --------------------------------------

    context = {}
    return HttpResponse(template.render(context, request))
```

# Step 4. ルート編集 - urls.py ファイル

以下の既存のファイルに、ソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄page2_patch2.html.txt
            ├── 📂views
            │   └── 📂practice
            │       └── 📄pages.py
👉          └── 📄urls.py
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

    # +----
    # | 練習

    # ...中略...

    # ページ２のパッチ２
    path('practice/page2_patch2',
         # --------------------
         # 1
         practice_pages.render_page2_patch2, name='page2_patch2'),
    #    ----------------------------------        ------------
    #    2                                         3
    # 1. 例えば `http://example.com/practice/page2_patch2` のような URL のパスの部分
    #                              ----------------------
    # 2. practice_pages (別名)ファイルの render_page2_patch2 メソッド
    # 3. HTMLテンプレートの中で {% url 'page2_patch2' %} のような形でURLを取得するのに使える

    # | 練習
    # +----
]
```

# Step 5. Webページにアクセスする

📖 [http://localhost:8000/practice/page2_patch2](http://localhost:8000/practice/page2_patch2)  

# 次の記事

📖 [Djangoでログイン／ログアウト機能を付けよう！](https://qiita.com/muzudho1/items/9f1ae4d0debc0b8aa4b1)  
