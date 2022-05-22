# 目的

ゲームルームを一覧したい。  

表示例:  

```plaintext
一覧表示
ID    部屋名        盤面       棋譜       アクション
----  -----------  ---------  ---------  ---------
1     Elephant     XOXOXOXOX  012345678  [観る]
2     Giraffe      XOXOXOXOX  012345678  [観る]
3     Lion         XOXOXOXOX  012345678  [観る]
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
        │   │   ├── 📂tic-tac-toe
        │   │   │   ├── 📂v1
        │   │   │   │   └── 📄<いろいろ>
        │   │   │   └── 📂v2
        │   │   │       ├── 📄connection.js
        │   │   │       ├── 📄engine.js
        │   │   │       ├── 📄game.js
        │   │   │       ├── 📄judge.js
        │   │   │       ├── 📄protocol_main.js
        │   │   │       └── 📄protocol_messages.js
        │   │   ├── 📂vuetify-practice
        │   │   │   └── 📄desserts.json
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂tic-tac-toe
        │   │       │   ├── 📂v1
        │   │       │   └── 📂v2
        │   │       │       ├── 📄portal.html
        │   │       │       └── 📄play.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
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
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂rooms
👉                      └── 📄list.html
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
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>部屋一覧</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <h3>部屋一覧</h3>
                    </v-container>
                    <v-container>
                        <v-simple-table>
                            <template v-slot:default>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>部屋名</th>
                                        <th>盤面</th>
                                        <th>棋譜</th>
                                        <th>アクション</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="room in vu_hotelDoc.rooms" :key="room.id">
                                        {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %} {% verbatim %}
                                        <td>{{ room.id }}</td>
                                        <td>{{ room.name }}</td>
                                        <td>{{ room.board }}</td>
                                        <td>{{ room.record }}</td>
                                        <td><v-btn :href="createRoomsReadPath(room.id)">観る</v-btn></td>
                                        {% endverbatim %}
                                    </tr>
                                </tbody>
                            </template>
                        </v-simple-table>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            var hotelDoc1 = JSON.parse("{{ dj_hotel|escapejs }}");
            // var hotelDocStr1 = JSON.stringify(hotelDoc1, null, "    ");
            // console.log(`hotelDocStr1=${hotelDocStr1}`);

            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印
                    vu_hotelDoc: hotelDoc1,
                    vu_readRoomPath: "{{ dj_readRoomPath }}",
                },
                methods: {
                    createRoomsReadPath(id) {
                        return `${this.vu_readRoomPath}${id}`;
                    },
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
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂rooms
            │           └── 📄list.html
            └── 📂views
👉              └── 📄v_room.py
```

```py
from django.shortcuts import render

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def render_list_room(request):
    """部屋一覧"""
    roomQuerySet = Room.objects.all().order_by('id')  # id 順にメンバーを全部取得
    dbRoomJsonStr = serializers.serialize('json', roomQuerySet)  # JSON 文字列に変換
    # Example:
    # dbRoomJsonStr=[{"model": "webapp1.room", "pk": 2, "fields": {"name": "Elephant", "board": "XOXOXOXOX", "record": "012345678"}}, {"model": "webapp1.room", "pk": 3, "fields": {"name": "Giraffe", "board": "XOXOXOXOX", "record": "012345678"}}, {"model": "webapp1.room", "pk": 5, "fields": {"name": "Gold", "board": "XOXOXOXOX", "record": "012345678"}}]
    # print(f"dbRoomJsonStr={dbRoomJsonStr}")

    dbRoomDoc = json.loads(dbRoomJsonStr)  # オブジェクトに変換
    # print(f"dbRoomDoc={json.dumps(dbRoomDoc, indent=4)}")
    """
    # Example
    dbRoomDoc=
    [
        {
            "model": "webapp1.room",
            "pk": 2,
            "fields": {
                "name": "Elephant",
                "board": "XOXOXOXOX",
                "record": "012345678"
            }
        },
        ...
    ]
    """

    # 使いやすい形に変換します
    resDoc = dict()
    resDoc["rooms"] = []

    for dbRecord in dbRoomDoc:
        # Example:
        # dbRecord= --> {'model': 'webapp1.room', 'pk': 2, 'fields': {'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}} <--
        # print(f"dbRecord= --> {dbRecord} <--")

        resDoc["rooms"].append(
            {
                "id": dbRecord["pk"],
                "name": dbRecord["fields"]["name"],
                "board": dbRecord["fields"]["board"],
                "record": dbRecord["fields"]["record"],
            }
        )

    # Example:
    # resDoc={'rooms': [{'id': 2, 'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}, {'id': 3, 'name': 'Giraffe', 'board': 'XOXOXOXOX', 'record': '012345678'}, {'id': 5, 'name': 'Gold', 'board': 'XOXOXOXOX', 'record': '012345678'}]}
    # print(f'resDoc={resDoc}')

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # 部屋がいっぱいあるので、名前はホテルとします
        # Vue には、 JSONオブジェクト を渡すのではなく、 JSON文字列 を渡します
        "dj_hotel": json.dumps(resDoc),
        # FIXME 相対パス。 URL を urls.py で変更したいとき、反映されないがどうするか？
        "dj_readRoomPath": "read/",
    }
    # Example:
    # context={'dj_hotel': '{"rooms": [{"id": 2, "name": "Elephant", "board": "XOXOXOXOX", "record": "012345678"}, {"id": 3, "name": "Giraffe", "board": "XOXOXOXOX", "record": "012345678"}, {"id": 5, "name": "Gold", "board": "XOXOXOXOX", "record": "012345678"}]}', 'dj_readRoom': 'rooms/read/'}
    print(f"context={context}")

    return render(request, "webapp1/rooms/list.html", context)
    #                       -----------------------
    #                       1
    # 1. webapp1/templates/webapp1/rooms/list.html
    #                      -----------------------
```

# Step 3. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂rooms
            │           └── 📄list.html
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
    path('rooms/', v_room.render_list_room, name='listRoom'),
    #     ------   -----------------------        ----------
    #     1        2                              3
    # 1. URLの `rooms/` というパスにマッチする
    # 2. v_room.py ファイルの render_list_room メソッド
    # 3. HTMLテンプレートの中で {% url 'listRoom' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

```shell
cd host1

# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/rooms/](http://localhost:8000/rooms/)  

# 次の記事

📖 [Djangoでゲーム対局部屋を読取しよう！](https://qiita.com/muzudho1/items/a39bea2f098951292916)  
