# 目的

（クライアント側ではなく）サーバー側に、データを記憶したい。  

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
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ構造を繰り返す
        │   │       └── 📄<いろいろ>.html
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

# Step 1. モデル作成 - m_member.py ファイル

以下のファイルを作成してほしい

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models
👉              └── 📄m_member.py
```

```py
# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models


class Member(models.Model):
    """会員"""

    # プロパティの仕様を決める感じで
    name = models.CharField('氏名', max_length=255)
    email = models.CharField('E-Mail', max_length=255)
    age = models.IntegerField('年齢', blank=True, default=0)

    # このオブジェクトを文字列にしたとき返るもの
    def __str__(self):
        return self.name
```

# Step 2. モデル作成 - コマンド実行

```shell
cd host1

docker-compose run --rm web python3 manage.py makemigrations webapp1
#                                                            -------
#                                                            1
# 1. アプリケーション ディレクトリー名
```

以下のディレクトリーとファイルが生成される。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂migrations
                ├── 📄__init__.py
                └── 📄0001_initial.py
```

👆 これらのファイルは マイグレーション ファイル と呼ぶらしい。  

# Step 3. コマンド実行＜その２＞

```shell
docker-compose run --rm web python manage.py migrate
```

👆 ここまでやって マイグレーション という作業が終わるらしい。  

# Step 4. admin.py を作成

以下のファイルを作成してほしい

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄__init__.py
            │   └── 📄0001_initial.py
            ├── 📂models
            │   └── 📄m_member.py
👉          └── 📄admin.py
```

```py
# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.contrib import admin
from .models.m_member import Member

# Register your models here.
admin.site.register(Member)
```

👆 管理画面に Member オブジェクトが表示されるようにしている。  

# Step 5. スーパーユーザーでWebの管理画面へアクセス

```shell
# Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

画面左に

```plain
WEBAPP1
Members +Add
```

のように表示されていればOK。  
されていなければ、スーパーユーザーでログインし直してほしい。  

# Step 6. Memberを３つほど追加してほしい

`Members +Add` の右側の `+Add` リンクをクリックしてほしい。  

```plaintext
氏名:
     ----------------

E-Mail:
       ----------------

年齢:
     ----

                [Save and add another] [Save and continue editing] [SAVE]
```

👆入力フォームが出てくるから、３件ほど適当に追加してほしい。  
`[SAVE]` が追加ボタンのようだ。  

# Step 7. 登録した Member を確認してほしい

`Members +Add` の `Members` リンクをクリックすると、一覧画面が出てくる。  

# 次の記事

📖 [Djangoでモデルのインスタンスの一覧表示をしよう！](https://qiita.com/muzudho1/items/77668130b6d941596327)  
