# 目的

何か所にも同じ HTML （＝ボイラープレート）があるような悪いコードを書く癖を止められる技術を早い学習段階で取得したい  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている  

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
        │   └── 📄urls.py
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        └── 📄urls.py
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 画面作成 - page2_base.html ファイル

以下のファイルを作成してほしい。

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂templates
                └── 📂webapp1
                    └── 📂practice
👉                      └── 📄page2_base.html
```

```html
<html>
    <head>
        <title>{% block title %}ページ２{% endblock %}</title>
    </head>
    <body>
        <!-- -->
        {% block section1 %}
        <h1>セクション１</h1>
        <p>コンテンツ１</p>
        {% endblock section1 %}

        <!-- -->
        {% block section2 %}
        <h1>セクション２</h1>
        <p>コンテンツ２</p>
        {% endblock section2 %}

        <!-- -->
        {% block section3 %}
        <h1>セクション３</h1>
        <p>コンテンツ３</p>
        {% endblock section3 %}
    </body>
</html>
```

# Step 3. 画面作成 - page2_patch1.html.txt ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂templates
                └── 📂webapp1
                    └── 📂practice
                        ├── 📄page2_base.html
👉                      └── 📄page2_patch1.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "practice/page2_base.html" %}
{#          ------------------------
            1
1. host1/webapp1/templates/webapp1/practice/page2_base.html
                                   ------------------------
#}

<!-- -->
{% block title %}ページ２（の１と２）{% endblock %}

<!-- -->
{% block section1 %}
    <h1>第１区画</1>
    <ul>
        <li>あ</li>
        <li>い</li>
        <li>う</li>
    </ul>
{% endblock section1 %}

<!-- -->
{% block section2 %}
    <h1>Section 2</h1>

    <table>
        <tr>
            <th></th>
            <th>A</th>
            <th>B</th>
            <th>C</th>
        </tr>
        <tr>
            {% block section2o1 %}
            <td>1</td>
            <td>ア</td>
            <td>イ</td>
            <td>ウ</td>
            {% endblock section2o1 %}
        </tr>
        <tr>
            <td>2</td>
            <td>エ</td>
            <td>オ</td>
            <td>カ</td>
        </tr>
        <tr>
            <td>3</td>
            <td>キ</td>
            <td>ク</td>
            <td>ケ</td>
        </tr>
    </table>
{% endblock section2 %}
```

# Step 4. ビュー作成 - pages.py ファイル

以下の既存のファイルに、ソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📂practice
            │           ├── 📄page2_base.html
            │           └── 📄page2_patch1.html.txt
            └── 📂views
                └── 📂practice
👉                  └── 📄pages.py
```

```py
from django.http import HttpResponse
from django.template import loader


# ...中略...


def render_page2_patch1(request):
    """ページ２　パッチ１"""
    template = loader.get_template('webapp1/practice/page2_patch1.html.txt')
    #                               --------------------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/page2_patch1.html.txt を取得
    #                            --------------------------------------

    context = {}
    return HttpResponse(template.render(context, request))
```


# Step 5. ルート編集 - urls.py ファイル

以下の既存のファイルに、ソースをマージしてほしい  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂templates
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           ├── 📄page2_base.html
        │   │           └── 📄page2_patch1.html.txt
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

    # +----
    # | 練習

    # ...中略...

    # ページ２のパッチ１
    path('practice/page2_patch1',
         # --------------------
         # 1
         practice_pages.render_page2_patch1, name='page2_patch1'),
    #    ----------------------------------        ------------
    #    2                                         3
    # 1. 例えば `http://example.com/practice/page2_patch1` のような URL のパスの部分
    #                              ----------------------
    # 2. practice_pages (別名)ファイルの render_page2_patch1 メソッド
    # 3. HTMLテンプレートの中で {% url 'page2_patch1' %} のような形でURLを取得するのに使える

    # | 練習
    # +----
]
```

# Step 6. Webページにアクセスする

📖 [http://localhost:8000/practice/page2_patch1](http://localhost:8000/practice/page2_patch1)  

# 次の記事

📖 [DjangoのHTMLのボイラープレートを減らすテンプレートを作るのも減らそう！](https://qiita.com/muzudho1/items/606d314c01543666c51b)  

# 参考にした記事

📖 [The Django template language](https://docs.djangoproject.com/en/4.0/ref/templates/language/) - これを読むのがよい  
