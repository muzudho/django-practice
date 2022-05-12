# 目的

（※いわゆる CRUD の R）  

`http://localhost:8000/rooms/read/1/` へアクセスすると、  
id が 1 の部屋を表示したい。  

表示例:  

```plaintext
部屋の詳細情報

名前
Elephant

盤面
+--+--+--+
| X|  |  |
+--+--+--+
|  | X|  |
+--+--+--+
| O| O| X|
+--+--+--+

棋譜
+----+
|   1|
+----+
|   7|
+----+
|   5|
+----+
|   8|
+----+
|   9|
+----+
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
        │   │   ├── 📂rooms
        │   │   │   └── 📄list.html
        │   │   └── 📂<いろいろ>-practice
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂tic_tac_toe1
        │   │   └── 📄consumer1.py
        │   ├── 📂tic-tac-toe2
        │   │   ├── consumer1.py
        │   │   └── protocol.py
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂websock_practice1
        │   │       └── 📂v1
        │   │           └── 📄consumer.py
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
👉                  └── 📄read.html
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" />
        <title>部屋読取</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <h3>部屋の詳細情報</h3>
                        <div class="card" style="width: 18rem">
                            <!-- 部屋名 -->
                            <div class="card-body">
                                <h5 class="card-title">部屋名</h5>
                                <p class="card-text">{{ room.name }}</p>
                            </div>
                            <!-- 盤面 -->
                            <div class="card-body">
                                <h5 class="card-title">盤面</h5>
                                <v-container>
                                    <v-row justify="center" dense>
                                        <v-col>
                                            {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %} {% verbatim %}
                                            <v-chip label color="grey lighten-4">{{label0}}</v-chip>
                                            <v-chip label color="grey lighten-4">{{label1}}</v-chip>
                                            <v-chip label color="grey lighten-4">{{label2}}</v-chip>
                                            {% endverbatim %}
                                        </v-col>
                                    </v-row>
                                    <v-row justify="center" dense>
                                        <v-col>
                                            {% verbatim %}
                                            <v-chip label color="grey lighten-4">{{label3}}</v-chip>
                                            <v-chip label color="grey lighten-4">{{label4}}</v-chip>
                                            <v-chip label color="grey lighten-4">{{label5}}</v-chip>
                                            {% endverbatim %}
                                        </v-col>
                                    </v-row>
                                    <v-row justify="center" dense>
                                        <v-col>
                                            {% verbatim %}
                                            <v-chip label color="grey lighten-4">{{label6}}</v-chip>
                                            <v-chip label color="grey lighten-4">{{label7}}</v-chip>
                                            <v-chip label color="grey lighten-4">{{label8}}</v-chip>
                                            {% endverbatim %}
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </div>
                            <!-- 棋譜 -->
                            <div class="card-body">
                                <v-card class="mx-auto" max-width="300" tile>
                                    <v-subheader>棋譜</v-subheader>
                                    <v-list dense class="overflow-y-auto" max-height="200">
                                        <v-list-item-group color="primary">
                                            <v-list-item v-for="(item, i) in record" :key="i">
                                                <v-list-item-content>
                                                    <v-list-item-title v-text="item"></v-list-item-title>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </v-list-item-group>
                                    </v-list>
                                </v-card>
                            </div>
                        </div>
                        <a href="{% url 'listRoom' %}" class="btn btn-default btn-sm">戻る</a>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            var board = "{{ room.board|escapejs }}";
            var record = "{{ room.record|escapejs }}";

            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    label0: board[0],
                    label1: board[1],
                    label2: board[2],
                    label3: board[3],
                    label4: board[4],
                    label5: board[5],
                    label6: board[6],
                    label7: board[7],
                    label8: board[8],
                    record: [parseInt(record[0]) + 1, parseInt(record[1]) + 1, parseInt(record[2]) + 1, parseInt(record[3]) + 1, parseInt(record[4]) + 1, parseInt(record[5]) + 1, parseInt(record[6]) + 1, parseInt(record[7]) + 1, parseInt(record[8]) + 1],
                },
            });
        </script>
    </body>
</html>
```

# Step 2. ビュー編集 - v_room.py ファイル

以下のファイルを編集してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂rooms
            │       └── 📄read.html
            └── 📂views
👉              └── 📄v_room.py
```

```py
from django.shortcuts import render

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def readRoom(request, id=id):
    """部屋読取"""
    context = {
        'room': Room.objects.get(pk=id),  # idを指定してメンバーを１人取得
    }
    return render(request, "rooms/read.html", context)
    #                       ---------------
    #                       1
    # 1. webapp1/templates/rooms/read.html
    #                      ---------------
```

# Step 3. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂rooms
            │       └── 📄read.html
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

    # 部屋読取
    path('rooms/read/<int:id>/', v_room.readRoom, name='readRoom'),
    #     --------------------   ---------------        ----------
    #     1                      2                      3
    # 1. URLの `rooms/read/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_room.py ファイルの readRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'readRoom' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

部屋番号は適宜変えてください  

📖 [http://localhost:8000/rooms/read/1/](http://localhost:8000/rooms/read/1/)  

# 次の記事

📖 [Djangoでゲーム対局部屋を削除しよう！](https://qiita.com/muzudho1/items/172485842e7adfb749aa)  
