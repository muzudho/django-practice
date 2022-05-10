# 目的

ゲームルームを一覧したい。  

表示例:  

```plaintext
一覧表示
ID    部屋名        盤面       棋譜
----  -----------  ---------  ---------
1     Elephant     XOXOXOXOX  012345678
2     Giraffe      XOXOXOXOX  012345678
3     Lion         XOXOXOXOX  012345678
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

参考にした元記事は 📖[DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    └── 📄<いろいろ>
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂tic-tac-toe1
        │   │   │   └── 📄<いろいろ>
        │   │   ├── 📂tic-tac-toe2
        │   │   │    ├── 📄connection.js
        │   │   │    ├── 📄engine.js
        │   │   │    ├── 📄game.js
        │   │   │    ├── 📄judge.js
        │   │   │    ├── 📄protocol_main.js
        │   │   │    └── 📄protocol_messages.js
        │   │   ├── 📂vuetify-practice
        │   │   │   └── 📄desserts.json
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂tic-tac-toe1
        │   │   │   └── 📄<いろいろ>
        │   │   ├── 📂tic-tac-toe2
        │   │   │   ├── 📄index.html
        │   │   │   └── 📄game.html
        │   │   └── 📂<いろいろ>-practice
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂tic_tac_toe1
        │   │   └── 📄consumer1.py
        │   ├── 📂tic-tac-toe2
        │   │   ├── consumer1.py
        │   │   └── protocol.py
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websock1
        │   │   ├── 📄consumer1.py
        │   │   └── 📄consumer2.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── 📄<いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── 📄<いろいろ>
```

# Step 1. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂rooms
👉                  └── 📄list.html
```

```html
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>部屋一覧</title>
        <!-- Bootstrap -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />
    </head>
    <body>
        <div class="container">
            <h3>部屋一覧</h3>

            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>部屋名</th>
                        <th>盤面</th>
                        <th>棋譜</th>
                    </tr>
                </thead>
                <tbody>
                    {% for room in rooms %}
                    <tr>
                        <td>{{ room.id }}</td>
                        <td>{{ room.name }}</td>
                        <td>{{ room.board }}</td>
                        <td>{{ room.record }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
</html>
```

# Step 2. ビュー編集 - v_room.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂rooms
            │       └── 📄list.html
            └── 📂views
👉              └── 📄v_room.py
```

```py
from django.http import HttpResponse
from django.template import loader

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def listRoom(request):
    """部屋一覧"""
    template = loader.get_template('rooms/list.html')
    context = {
        'rooms': Room.objects.all().order_by('id'),  # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))
```

# Step 3. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂rooms
            │       └── 📄list.html
            ├── 📂views
            │   └── 📄v_room.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_room
#    ------- -----        ------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # 部屋一覧
    path('rooms/', v_room.listRoom, name='listRoom'),
    #     ------   ---------------        ----------
    #     1        2                      3
    # 1. URLの `rooms/` というパスにマッチする
    # 2. v_room.py ファイルの listRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'listRoom' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/rooms/](http://localhost:8000/rooms/)  

# 次の記事
