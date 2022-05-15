# 目的

ロビー（待合室）を作りたい。  
そこには　部屋の一覧と、　アクティブ ユーザー の一覧がある。  

ただし、まだ用意していないため、  
部屋のデータは 現在対局中のものを反映しておらず 仮のものとし、  
アクティブ ユーザーも 現在 対局中かどうかの状態を保持していない。  

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
    ├── 📂host_local1
    │    └── 📄<いろいろ>
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂models_helper
        │   │   └── 📄mh_session.py
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
        │   │   └── 📂tic-tac-toe
        │   │       ├── 📂v1
        │   │       │   └── 📄<いろいろ>
        │   │       ├── 📂v2
        │   │       │   ├── 📄match_request.html
        │   │       │   └── 📄play.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   ├── 📄v_tic_tac_toe_v1.py
        │   │   ├── 📄v_tic_tac_toe_v2.py
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       │   └── 📄consumer.py
        │   │       └── 📂v2
        │   │           ├── 📄consumer.py
        │   │           └── 📄protocol.py
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

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. モデル関連作成 - mh_room.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models_helper
👉              └── 📄mh_room.py
```

```py
import json
from django.core import serializers


from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def get_all_rooms():
    # id順に要素を全部取得
    dbRoomQuerySet = Room.objects.all().order_by('id')
    # roomSet=<QuerySet [<Room: Elephant>, <Room: Giraffe>, <Room: Gold>]>
    print(f"dbRoomQuerySet={dbRoomQuerySet}")

    # JSON 文字列に変換
    dbRoomJsonStr = serializers.serialize('json', dbRoomQuerySet)

    # オブジェクトに変換
    dbRoomDoc = json.loads(dbRoomJsonStr)

    # 使いやすい形に変換します
    hotelDic = dict()
    for dbRoom in dbRoomDoc:

        # Example:
        # dbRoom= --> {'model': 'webapp1.room', 'pk': 2, 'fields': {'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}} <--
        print(f"dbRoom= --> {dbRoom} <--")

        hotelDic[dbRoom["pk"]] = {
            "pk": dbRoom["pk"],
            "name": dbRoom["fields"]["name"],
            "board": dbRoom["fields"]["board"],
            "record": dbRoom["fields"]["record"],
        }

    return hotelDic
```

# Step 2. ビュー編集 - v_lobby_v1.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
👉              └── 📄v_lobby_v1.py
```

```py
import json
from django.http import HttpResponse
from django.template import loader

from webapp1.models_helper.mh_room import get_all_rooms
#    ------- ------------- -------        -------------
#    1       2             3              4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 関数名


from webapp1.models_helper.mh_session import get_all_logged_in_users
#    ------- ------------- ----------        -----------------------
#    1       2             3                 4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 関数名


def render_lobby(request):
    """ロビー（待合室）"""
    template = loader.get_template('lobby/v1/lobby.html')
    #                               -------------------
    #                               1
    # 1. webapp1/templates/lobby/v1/lobby.html
    #                      -------------------

    # 部屋の一覧
    hotelDic = get_all_rooms()

    # ユーザーの一覧
    usersDic = get_all_logged_in_users()

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # 部屋がいっぱいあるからホテル
        'dj_hotel': json.dumps(hotelDic),
        # 人がいっぱいいるからパーク
        'dj_park': json.dumps(usersDic),
        # FIXME 相対パス。 URL を urls.py で変更したいとき、反映されないがどうするか？
        "dj_pathOfHome": "home/v2/",
        "dj_pathOfRoomsRead": "rooms/read/",
    }

    return HttpResponse(template.render(context, request))
```

# Step 3. テンプレート編集 - lobby.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models
            │   ├── 📄m_state_in_park.py
            │   └── 📄m_member.py
            ├── 📂templates
            │   └── 📂lobby
            │       └── 📂v1
👉          │           └── 📄lobby.html
            └── 📂views
                └── 📄v_lobby_v1.py
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
        <title>ロビー（待合室）</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <!-- v-app-bar に app プロパティを指定しないなら、背景画像を付けてほしい -->
                <v-app-bar app dense elevation="4">
                    <v-app-bar-nav-icon></v-app-bar-nav-icon>
                    <v-toolbar-title>ゲーム対局サーバー</v-toolbar-title>
                    <v-spacer></v-spacer>
                    <v-btn class="my-4" color="primary" :href="createPathOfHome()">自分のホームへ帰る</v-btn>
                </v-app-bar>
                <v-main>
                    <v-container>
                        <h2>ロビー（待合室）</h2>
                        <h3>部屋一覧</h3>
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
                                    <tr v-for="room in vu_hotelDoc" :key="room.pk">
                                        {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %} {% verbatim %}
                                        <td>{{ room.pk }}</td>
                                        <td>{{ room.name }}</td>
                                        <td>{{ room.board }}</td>
                                        <td>{{ room.record }}</td>
                                        <td><v-btn :href="createPathOfRoomsRead(room.pk)">観る</v-btn></td>
                                        {% endverbatim %}
                                    </tr>
                                </tbody>
                            </template>
                        </v-simple-table>
                    </v-container>
                    <v-container>
                        <h3>アクティブ ユーザー一覧</h3>
                        <v-simple-table>
                            <template v-slot:default>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>参加者名</th>
                                        <th>アクティブか</th>
                                        <th>最終ログイン</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in vu_parkDoc" :key="user.pk">
                                        {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %} {% verbatim %}
                                        <td>{{ user.pk }}</td>
                                        <td>{{ user.username }}</td>
                                        <td>{{ user.is_active }}</td>
                                        <td>{{ user.last_login }}</td>
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
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印
                    // 部屋がいっぱいあるからホテル
                    vu_hotelDoc: JSON.parse("{{ dj_hotel|escapejs }}"),
                    // 人がいっぱいいるからパーク
                    vu_parkDoc: JSON.parse("{{ dj_park|escapejs }}"),

                    vu_pathOfHome: "{{ dj_pathOfHome }}",
                    vu_pathOfRoomsRead: "{{ dj_pathOfRoomsRead }}",
                },
                methods: {
                    createPathOfHome() {
                        let path = `${location.protocol}//${location.host}/${this.vu_pathOfHome}`;
                        //          --------------------  ---------------- ---------------------
                        //          1                     2                3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`room path=[${path}]`);
                        return path;
                    },
                    createPathOfRoomsRead(roomId) {
                        let path = `${location.protocol}//${location.host}/${this.vu_pathOfRoomsRead}${roomId}`;
                        //          --------------------  ---------------- -----------------------------------
                        //          1                     2                3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`room path=[${path}]`);
                        return path;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models
            │   ├── 📄m_state_in_park.py
            │   └── 📄m_member.py
            ├── 📂templates
            │   └── 📂lobby
            │       └── 📂v1
            │           └── 📄lobby.html
            ├── 📂views
            │   └── 📄v_lobby_v1.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_lobby_v1
#    ------- -----        ----------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # ロビー（待合室）
    path('lobby/v1/', v_lobby_v1.render_lobby, name='lobbyV1_lobby'),
    #     ---------   -----------------------        -------------
    #     1           2                              3
    #
    # 1. URLの `lobby/v1/` というパスにマッチする
    # 2. v_lobby_v1.py ファイルの render_lobby メソッド
    # 3. HTMLテンプレートの中で {% url 'lobbyV1_lobby' %} のような形でURLを取得するのに使える
]
```

# Step 5. Web画面へアクセス

📖 [http://localhost:8000/lobby/v1/](http://localhost:8000/lobby/v1/)  

# 関連する記事

📖 [djangoでログイン状態を判定する機能](https://techpr.info/python/django-login-judge/)  
📖 [DjangoのUserモデルを拡張する方法](https://hodalog.com/how-to-extend-django-user-model/)  