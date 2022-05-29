# 目的

サーバーに、部屋を記憶したい  

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
わたしの記事は単に **やってみた** ぐらいの位置づけだ  

ディレクトリ構成を抜粋すると 以下のようになっている  

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

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. モデル作成 - m_member.py ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models
👉              └── 📄m_room.py
```

```py
# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models


class Room(models.Model):
    """部屋のモデル"""

    # プロパティの仕様を決める感じで

    # 部屋名
    # -----
    # Example: Elephant
    name = models.CharField('部屋名', max_length=25)

    # 対局者_先手Id
    # ------------
    # Example: 1
    sente_id = models.IntegerField('対局者_先手Id', null=True, blank=True)

    # 対局者_後手Id
    # ------------
    # Example: 2
    gote_id = models.IntegerField('対局者_後手Id', null=True, blank=True)

    # 盤面
    # ----
    # Example: ..O.X.X..
    # +--+--+--+
    # |  |  | O|
    # +--+--+--+
    # |  | X|  |
    # +--+--+--+
    # | X|  |  |
    # +--+--+--+
    board = models.CharField('盤面', max_length=9)

    # 棋譜
    # ----
    # Example: 426
    record = models.CharField('棋譜', max_length=9)

    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return self.name
```

# Step 3. コマンド実行

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

docker-compose run --rm web python3 manage.py makemigrations webapp1
#                                                            -------
#                                                            1
# 1. アプリケーション ディレクトリー名
```

以下のディレクトリーとファイルが生成される  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄<いろいろ>.py
👉          │   └── 📄0003_room.py          # このファイル名は変わります
            └── 📂models
                └── 📄m_room.py
```

👆 これらのファイルは マイグレーション ファイル と呼ぶらしい  

# Step 4. コマンド実行＜その２＞

```shell
docker-compose run --rm web python manage.py migrate
```

👆 ここまでやって マイグレーション という作業が終わるらしい  

# Step 5. admin.py を編集

以下のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄<いろいろ>.py
            │   └── 📄0003_room.py
            ├── 📂models
            │   └── 📄m_room.py
👉          └── 📄admin.py
```

👇 追加したものだけ示す  

```py
# 冒頭
from .models.m_room import Room

# ...中略...

# Register your models here.
admin.site.register(Room)
```

👆 管理画面に Room オブジェクトが表示されるようにしている。  

# Step 6. スーパーユーザーでWebの管理画面へアクセス

```shell
# Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

画面左に

```plain
WEBAPP1
Members  +Add ✏Change
Desserts +Add ✏Change
Rooms    +Add ✏Change
```

のように表示されていればOK。  
されていなければ、スーパーユーザーでログインし直してほしい。  

# Step 7. Room を３つほど追加してほしい

`Rooms    +Add` の右側の `+Add` リンクをクリックしてほしい。  

```plaintext
部屋名:
      ----------------

対局者_先手Id:
             ----------------

対局者_後手Id:
             ----------------

盤面:
    ----------------

棋譜:
    ----

                [Save and add another] [Save and continue editing] [SAVE]
```

👆入力フォームが出てくるから、３件ほど適当に追加してほしい。  

入力例:  

```plaintext
部屋名        対局者_先手Id  対局者_後手Id  盤面       棋譜
-----------  ------------  ------------  ---------  ---------
Elephant                1             2  XOXOXOXOX  012345678
Giraffe                 3             4  XOXOXOXOX  012345678
Lion                    5             6  XOXOXOXOX  012345678
```

`[SAVE]` が追加ボタンのようだ。  

# Step 8. 登録した Room を確認してほしい

`Rooms    +Add` の `Rooms` リンクをクリックすると、一覧画面が出てくる。  

# 次の記事

📖 [Djangoでゲーム対局部屋を一覧しよう！](https://qiita.com/muzudho1/items/346c286d4f99850afe23)  
