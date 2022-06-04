# 目的

Webサイトのポータルページを作成したい  

以下のようなURLで表示させる  

```plain
http://<省略>.com/
------]---------]
1      2

1. プロトコル
2. ホスト
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
        │   │   ├── 📂allauth-customized
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

# Step 1. 画面作成 - index.html ファイル

以下のファイルを作成してほしい。

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂templates
                └── 📂webapp1
👉                  └── 📄index.html
```

👇 下のハイパーリンクの先にはまだページを作っていない。 レッスンの進み具合によって変えてほしい  

```html
<html>
    <head>
        <title>ポータル ページ</title>
    </head>
    <body>
        Webサイト作成の練習中です。<br/>
        <br/>
        <a href="home/v1/">ホーム</a>
    </body>
</html>
```

# Step 2. ビュー作成 - v_index.py ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📄index.html
            └── 📂views
👉              └── 📄v_index.py
```

```py
from django.http import HttpResponse
from django.template import loader


def render_index(request):
    template = loader.get_template('webapp1/index.html')
    #                               ------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/index.html を取得
    #                            ------------------

    context = {}
    return HttpResponse(template.render(context, request))

    # HTML をハードコーディングすることもできる
    # return HttpResponse("""Hello, world. You're at the webapp1 index.<br/>
    #                    <a href="home/v1/">ホーム</a>""")
```

# Step 3. ルート編集 - urls.py

以下のファイルが無ければ新規作成、あれば編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📄index.html
            ├── 📂views
            │   └── 📄v_index.py
👉          └── 📄urls.py
```

```py
# 冒頭
from django.urls import path

from webapp1.views import v_index
#    ------- -----        -------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

# 追記
urlpatterns = [
    # ...中略...

    # ポータル
    path('', v_index.render_index, name='index'),
    #    --  --------------------        -----
    #    1   2                           3
    # 1. 例えば `http://example.com/` のように、 URLのパスの部分を指定しなかったケースに対応します
    # 2. v_index.py ファイルの render_index メソッド
    # 3. HTMLテンプレートの中で {% url 'index' %} のような形でURLを取得するのに使える
]
```

# Step 4. Webページにアクセスする

📖 [http://localhost:8000/](http://localhost:8000/)  

# 次の記事

📖 [DjangoでWebページを追加しよう！](https://qiita.com/muzudho1/items/06fe071c1147b4b8f062)  
