---
title: Djangoでモデルを追加しよう！
tags: Django Docker
author: muzudho1
slide: false
---
# 目的

サーバーにデータを記憶したい。  
データの形のようなものを **モデル** と呼ぶ。モデルを決めるとサーバーにデータを保存できるようになる。  
モデルの決め方、データの追加の仕方を説明する。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                              | Value                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------ |
| スーパーユーザーを作っておくこと | 📖[Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153) |

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

参考にした元記事は 📖[DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📂templates
　│　　│    └── 📂webapp1
　│　　│        └── 📄<いろいろ>.html
　│　　├── 📄settings.py
　│　　├── 📄urls.py
　│　　├── 📄views.py
　│　　└── <いろいろ>
　├── 📄.env
　├── 🐳docker-compose.yml
　├── 🐳Dockerfile
　├── 📄manage.py
　└── <いろいろ>
```

# Step 1. models.py を作成

以下のファイルを作成してほしい

📄`host1/webapp1/models.py`:  

```py
# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models

# 任意のオブジェクトの仕様を決める感じで
class Member(models.Model):

    # プロパティの仕様を決める感じで
    name = models.CharField('氏名', max_length=255)
    email = models.CharField('E-Mail', max_length=255)
    age = models.IntegerField('年齢', blank=True, default=0)

    # このオブジェクトを文字列にしたとき返るもの
    def __str__(self):
        return self.name
```

# Step 2. コマンド実行

```shell
cd host1

docker-compose run --rm web python3 manage.py makemigrations webapp1
#                                                            -------
#                                                            1
# 1. アプリケーション ディレクトリー名
```

以下のディレクトリーとファイルが生成される。  

```plaintext
📂host1
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

📄`host1/webapp1/admin.py`:  

```py
# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.contrib import admin
from .models import Member

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
