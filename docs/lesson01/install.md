---
title: DjangoをDockerコンテナへインストールしよう！
tags: Windows VisualStudioCode Docker Django コンテナ
author: muzudho1
slide: false
---
# 目的

会員制のWebサイトのデモを作ることになった。  
要件のうち特筆すべきは次の１点  

* 身内でメンテナンスできる人を集めやすいプログラム言語、フレームワークを使ってほしい

ちなみにうちは 人工知能分野で、機械学習をしている人が多い。  
**Python** を使える人が多いから **Django** はすぐに思いついた。  

また、（要件に反するが）四の五の言わさず **Docker** を押し付けることにした。  

# はじめに

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |
| Database  | PostgreSQL                                |

一番参考になる元記事は 📖[Quickstart: Compose and Django](https://docs.docker.com/samples/django/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

# Step 1. 開発環境の確認

VSCode のターミナルで以下のコマンドを叩いていって、この記事と環境が似ているか確認してほしい。  

```shell
python -V
```

`Python 3.9.10`  

```shell
docker --version
```

`Docker version 20.10.10, build b485636`  

```shell
docker-compose -version
```

`docker-compose version 1.29.2, build 5becea4c`  

```shell
# pip を最新に
python -m pip install --upgrade pip
```

# Step 2. ディレクトリとファイルの作成

次に、ディレクトリ１つと、ファイル３つは　最低限　自分で用意する必要がある。  
コピー貼り付けでもして、以下のディレクトリー構成を作ってほしい。  

```plain
📂host1
　├── 📄docker-compose.yml
　├── 📄Dockerfile
　└── 📄requirements.txt
```

`host1` という名前は、プロジェクトの名前を入れてほしい。  

📄`host1/requirements.txt`:  

```plaintext
# Dockerはまだ Django 4 に対応してない？
Django>=3.0,<4.0

# PostgreSQLへ接続するためのドライバ
psycopg2>=2.8
```

📄`host1/Dockerfile`:  

```Dockerfile
# See also: https://docs.docker.com/samples/django/

FROM python:3

# Pythonのキャッシュファイル（__pycache__ディレクトリや.pycファイル）を作成するのを止めます
ENV PYTHONDONTWRITEBYTECODE=1

# 出力をPythonでバッファリングせずにターミナルに直接送信します
ENV PYTHONUNBUFFERED=1

# コンテナに /code ディレクトリを作成し、以降、 /code ディレクトリで作業します
WORKDIR /code

# requirements.txtを /code/ ディレクトリへコピーします
ADD requirements.txt /code/

# requirements.txtに従ってpip installします
RUN pip install -r requirements.txt

# 開発環境のファイルを /code/ へコピーします
COPY . /code/
```

📄`host1/docker-compose.yml`:

```yaml
version: "3.9"

services:
  # データベース
  db:
    image: postgres
    volumes:
      - ./data/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  # Djangoアプリ
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    #                                   -------
    #                                   1
    # 1. Dockerコンテナ内のサーバーは localhost ではなく 0.0.0.0 と書く
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    depends_on:
      - db
```

# Step 3. コマンド実行

次に、作ったディレクトリーへ下りてほしい。  

```shell
cd host1
```

そして、以下のコマンドを１回だけ叩いてほしい。  

```shell
docker-compose run web django-admin.py startproject webapp1 .
#                                                   -------
#                                                   任意のWebアプリケーションのフォルダー名
```

すると、以下のものが自動生成される。  

```plain
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📄__init__.py
　│　　├── 📄asgi.py
　│　　├── 📄settings.py
　│　　├── 📄urls.py
　│　　└── 📄wsgi.py
　└── 📄manage.py
```

# Step 4. settings.pyの編集

そしたら、以下の部分を編集してほしい。  

📄host1/webapp1/settings.py:  

```py
import os # 冒頭のあたりに追加

# 以下を書きかえてください
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

# Step 5. もう一度コマンド実行

次に、以下のコマンドを叩いてほしい。  

```shell
docker-compose up
```

# Step 6. Webページへアクセス

次に、ブラウザで以下のURLにアクセスしてほしい。  

[http://localhost:8000](http://localhost:8000)  

これで、ロケットが飛んでいるページが出てくれば　インストールは完了だ。  
`[Ctrl]+[C]` キーでWebサーバーを停めることができる。  

# 次の記事

学習コストが低くなるように並べてあります。数字の小さな Lesson から読み進めてください。  

Lesson 1. Install  

* 📖 `DjangoをDockerコンテナへインストールしよう！` (この記事)  

Lesson 2. Auth  

* 📖 [Djangoでユーザー認証を付けよう！](https://qiita.com/muzudho1/items/55cb7ac55299afd51887)

Lesson 3. Page  

* 📖 [DjangoでWebページを追加しよう！](https://qiita.com/muzudho1/items/06fe071c1147b4b8f062)
    * 📖 [Djangoでログインユーザー情報を表示しよう！](https://qiita.com/muzudho1/items/9f1ae4d0debc0b8aa4b1)

Lesson 4. Super-user  

* 📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)

Lesson 5. Model  

* 📖 [Djangoでモデルを追加しよう！](https://qiita.com/muzudho1/items/2463cc006da69f5ed7b2)

Lesson 6. CRUD  

* 📖 [Djangoでモデルのインスタンスの一覧表示をしよう！](https://qiita.com/muzudho1/items/77668130b6d941596327)
    * 📖 [Djangoでモデルのインスタンスの読取ページを作成しよう！](https://qiita.com/muzudho1/items/ae362f53a670e265a7e4)
    * 📖 [Djangoでモデルのインスタンスの削除ページを作成しよう！](https://qiita.com/muzudho1/items/32694c883331c75ef059)
    * 📖 [Djangoでモデルのインスタンスの作成／更新ページを作成しよう！](https://qiita.com/muzudho1/items/806ecdba1654ae169f37)

Lesson 7. Vuetify

* 📖 [DjangoでフロントサイドにVuetifyを使おう！](https://qiita.com/muzudho1/items/e80a72b027249daa4d41)
    * 📖 [DjangoでVuetifyのData tableを使おう！](https://qiita.com/muzudho1/items/2b01d3acce5ec1b5770b)

Lesson 8. JSON

* 📖 [Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1)
    * 📖 [DjangoのWebページへJSON形式のテキストを渡そう！](https://qiita.com/muzudho1/items/c50859d9bde800d06a62)
* 📖 [DjangoのサーバーからデータをJSON形式のテキストで受信しよう！](https://qiita.com/muzudho1/items/d83760a6a4abadaf19c4)
* 📖 [DjangoでデータをサーバーへJSON形式で渡して、記憶させよう！](https://qiita.com/muzudho1/items/ed0ea262aaa327a2d12b)

Lesson 9. Socket

* 📖 [ソケットを使おう！](https://qiita.com/muzudho1/items/7a6501f7dbafbaa9b96c)

Lesson 10. Web socket

* 📖 [DjangoのWebサーバーとクライアント側のアプリで通信しよう！](https://qiita.com/muzudho1/items/9bad88a4092bf83a0f12)
    * 📖 [DjangoのWebサーバーとクライアント側のアプリ間でJSON形式のテキストを通信しよう！](https://qiita.com/muzudho1/items/a3870c78f609a65debe0)

Lesson 11. Tic tac toe

* 📖 [Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！](https://qiita.com/muzudho1/items/3bd5e55fbea2c0598e8b)
