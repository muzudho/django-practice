# 目的

ゲーム対局部屋にチェックインしたい  

そこで、  
ゲーム対局部屋に入るときは当該 Room モデルのレコードの sente_id または gote_id フィールドに 自分のユーザーIdを上書きし、  
自分の Profile レコードの match_state フィールドを 3 （対局中）に上書きする  

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
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   ├── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │   │   └── 📂practice
        │   │   │       └── 📄<いろいろ>.js
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂tic-tac-toe
        │   │       │   ├── 📂v1
        │   │       │   └── 📂v2
        │   │       │       └── 📄<いろいろ>.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           └── 📄<いろいろ>.py
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

# Step 2. ビュー編集 - v_tic_tac_toe_v3.py ファイル

以下の既存のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
👉              └── v_tic_tac_toe_v3.py
```

```py
from django.http import Http404
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User # デバッグ用

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.models.m_user_profile import Profile
#    ------- ------ --------------        -------
#    1       2      3                     4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MatchApplication():

    # ...中略...

    @classmethod
    def on_sent(clazz, request):
        """送信後"""

        # Specification
        #
        # ログインしていないユーザーが部屋に入っても 何も記録しません
        #
        # ログインしているユーザーが部屋に入ってくると、以下のものを記録します（チェックイン）
        #
        # * Room.sente_id または Room.gote_id の空いている方に user.pk を上書き
        # * user.profile.match_state を 3 （対局中）に上書き

        # `po_` は POST送信するパラメーター名の目印
        # 部屋名
        po_room_name = request.POST.get("po_room_name")
        # 自分の駒。 X か O
        po_my_piece = request.POST.get("po_my_piece")

        # 部屋の取得 または 新規作成
        #
        # * ID ではなく、部屋名から行う
        room_table_qs = Room.objects.filter(name=po_room_name)
        # print(
        #     f"[MatchApplication on_sent] po_room_name=[{po_room_name}] len={len(room_table_qs)}")

        if 1 <= len(room_table_qs):
            # （名前被りがあったなら）先頭の１つを取得
            room = room_table_qs[0]
            # print(f"[MatchApplication on_sent] first room=[{room}]")
            # print(
            #     f"[MatchApplication on_sent] first room .name=[{room.name}] .sente_id=[{room.sente_id}] .gote_id=[{room.gote_id}] .board=[{room.board}] .record=[{room.record}]")
        else:
            # 新規作成
            room = Room()
            room.name = po_room_name
            # print(f"[MatchApplication on_sent] new room=[{room}]")

        # print(f"[MatchApplication on_sent] request.user={request.user}")
        # print(
        #     f"[MatchApplication on_sent] request.user.is_authenticated={request.user.is_authenticated}")

        if request.user.is_authenticated:
            # ログインしたユーザーだった

            user_pk = request.user.pk
            # print(
            #     f"[MatchApplication on_sent] user_pk={user_pk} room.sente_id={room.sente_id} room.gote_id={room.gote_id}")

            # デバッグ
            # user = User.objects.get(pk=user_pk)
            # print(
            #     f"[MatchApplication on_sent] user username={user.username}")

            # 自分の Profile レコード 取得
            profile = Profile.objects.get(user__pk=user_pk)
            #                             --------
            #                             1
            # 1. Profile テーブルと 1対1 で紐づいている親テーブル User の pk フィールド

            # print(f"[MatchApplication on_sent] profile={profile}")
            # print(
            #     f"[MatchApplication on_sent] profile.match_state={profile.match_state}")

            if po_my_piece == "X":
                # X を取った方は先手とします
                room.sente_id = user_pk
                # ユーザーの状態を対局中（3）にします
                profile.match_state = 3

            elif po_my_piece == "O":
                # O を取った方は後手とします
                #
                # * 先手と後手が同じユーザーでも構わないものとします
                room.gote_id = user_pk
                # ユーザーの状態を対局中（3）にします
                profile.match_state = 3

            else:
                # それ以外は観戦者として扱う
                # ユーザーの状態を観戦中（4）にします
                profile.match_state = 4

            # 先手と後手の両方が埋まったなら
            if not(room.sente_id is None or room.sente_id == 0 or room.gote_id is None or room.gote_id == 0):
                # 盤と棋譜を空っぽにする
                room.board = ""
                room.record = ""

            # print(
            #     f"[MatchApplication on_sent] room .name=[{room.name}] .sente_id=[{room.sente_id}] .gote_id=[{room.gote_id}] .board=[{room.board}] .record=[{room.record}]")
            # TODO バリデーションチェック
            room.save()

            # print(
            #     f"[MatchApplication on_sent] prifile .match_state=[{profile.match_state}]")
            # TODO バリデーションチェック
            profile.save()

            # print(f"[MatchApplication on_sent] ★ 更新終わり")
        else:
            # ゲストだった
            # print(f"[MatchApplication on_sent] ★ ゲスト")
            pass
```

# Step 3. Web画面へアクセス

* このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください
* テストするためには `サインアップ` してアカウントを作ってから、 `ログイン` してください
* 最初のテストは　既存でない部屋名で、次のテストは　既存の部屋名　で行うといいかもしれません

📖 [http://localhost:8000/accounts/v1/signup/](http://localhost:8000/accounts/v1/signup/)  
📖 [http://localhost:8000/accounts/v1/login/](http://localhost:8000/accounts/v1/login/)  
📖 [http://localhost:8000/tic-tac-toe/v3/match-application/](http://localhost:8000/tic-tac-toe/v3/match-application/)  

部屋、ユーザーを確認するには、管理画面を使うのが確実です:  

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

# 参考にした記事

📖 [Create Django model or update if exists](https://stackoverflow.com/questions/14115318/create-django-model-or-update-if-exists)  
📖 [How can I get the username of the logged-in user in Django?](https://stackoverflow.com/questions/16906515/how-can-i-get-the-username-of-the-logged-in-user-in-django)  
