# 目的

現在、サーバーに接続しているソケット（≒アクティブ・ユーザー）を一覧したい。  
ログアウトせず、まだセッション期限切れではなく　放置されているソケットを数えても構わないものとする。  

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

# Step 2. モデル関連作成 - mh_session.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models_helper
👉              └── 📄mh_session.py
```

```py
# See also: 📖[How to get the list of the authenticated users?](https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users)
import json
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core import serializers
from django.utils import timezone


def get_all_logged_in_users():
    # 接続が切れていないセッションを絞りこみます。
    # ログアウトせず２週間放置しているセッションが含まれる場合があります
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # セッション一覧を、ユーザーID一覧に変換します
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # ユーザーID一覧を使って、ユーザーを絞りこみます
    dbUsersQuerySet = User.objects.filter(id__in=uid_list)
    # users=<QuerySet [<User: kifuwarabe>]>
    # print(f"dbUsersQuerySet={dbUsersQuerySet}")

    # JSON 文字列に変換
    dbUsersJsonStr = serializers.serialize('json', dbUsersQuerySet)
    # print(f"dbUsersJsonStr={dbUsersJsonStr}")

    # オブジェクトに変換
    dbUserDoc = json.loads(dbUsersJsonStr)
    """
web_1  | dbUserDoc=[
web_1  |     {
web_1  |         "model": "auth.user",
web_1  |         "pk": 1,
web_1  |         "fields": {
web_1  |             "password": "pbkdf2_sha256$260000$tOSdFO6BqvafBgtFgE1qYS$+rv007MKnAy8j+krixlQuogvi46Xl8fZf87xn4lAU+0=",
web_1  |             "last_login": "2022-05-14T03:09:21.968Z",
web_1  |             "is_superuser": false,
web_1  |             "username": "kifuwarabe",
web_1  |             "first_name": "",
web_1  |             "last_name": "",
web_1  |             "email": "muzudho1@gmail.com",
web_1  |             "is_staff": false,
web_1  |             "is_active": true,
web_1  |             "date_joined": "2022-03-13T05:45:26.368Z",
web_1  |             "groups": [],
web_1  |             "user_permissions": []
web_1  |         }
web_1  |     }
web_1  | ]
    """
    # print(f"dbUserDoc={json.dumps(dbUserDoc, indent=4)}")

    # 使いやすい形に変換します
    usersDic = dict()
    for dbUser in dbUserDoc:
        usersDic[dbUser["pk"]] = {
            "pk": dbUser["pk"],
            "last_login": dbUser["fields"]["last_login"],
            "username": dbUser["fields"]["username"],
            "is_active": dbUser["fields"]["is_active"],
        }

    return usersDic
```

# Step 3. ビュー編集 - v_session_practice_v1.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models_helper
            │   └── 📄mh_session.py
            └── 📂views
👉              └── 📄v_session_practice_v1.py
```

```py
import json
from django.shortcuts import render

from webapp1.models_helper.mh_session import get_all_logged_in_users
#    ------- ------------- ----------        -----------------------
#    1       2             3                 4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 関数名


def renderActiveUserList(request):
    """アクティブ ユーザー一覧"""

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # Vue に渡すときは、 JSON オブジェクトではなく、 JSON 文字列です
        'dj_users': json.dumps(get_all_logged_in_users())
    }
    return render(request, "session-practice/active-user-list.html", context)
    #                       --------------------------------------
    #                       1
    # 1. webapp1/templates/session-practice/active-user-list.html
    #                      --------------------------------------
```

# Step 4. テンプレート編集 - active-user-list.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models_helper
            │   └── 📄mh_session.py
            ├── 📂templates
            │   └── 📂lobby
            │       └── 📂v1
👉          │           └── active-user-list.html
            └── 📂views
                └── 📄v_session_practice_v1.py
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
                                        <th>ユーザー名</th>
                                        <th>アクティブか</th>
                                        <th>最終ログイン</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in vu_users" :key="user.pk">
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
                    vu_users: JSON.parse("{{ dj_users|escapejs }}"),
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

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models_helper
            │   └── 📄mh_session.py
            ├── 📂templates
            │   └── 📂lobby
            │       └── 📂v1
            │           └── active-user-list.html
            ├── 📂views
            │   └── 📄v_session_practice_v1.py
👉          └── 📄urls.py
```

```py
from webapp1.views import v_session_practice_v1
#    ------- -----        ---------------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # アクティブ ユーザー一覧
    path('session-practice/v1/active-user-list/',
         # ------------------------------------
         # 1
         v_session_practice_v1.renderActiveUserList, name='sessionPracticeV1_activeUserList'),
    #    --------------------- --------------------        --------------------------------
    #     1                    2                           3
    #
    # 1. URLの `session-practice/v1/active-user-list/` というパスにマッチする
    # 2. v_session_practice_v1.py ファイルの renderActiveUserList メソッド
    # 3. HTMLテンプレートの中で {% url 'sessionPracticeV1_activeUserList' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/session-practice/v1/active-user-list/](http://localhost:8000/session-practice/v1/active-user-list/)  

# 関連する記事

📖 [djangoでログイン状態を判定する機能](https://techpr.info/python/django-login-judge/)  
📖 [How to get the list of the authenticated users?](https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users)  
📖 [Get List of Current Users](https://www.codingforentrepreneurs.com/blog/django-tutorial-get-list-of-current-users)  
