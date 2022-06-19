# 目的

環境を用意する  

# はじめに

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |
| Database  | PostgreSQL                                |

一番参考になる元記事は 📖[Quickstart: Compose and Django](https://docs.docker.com/samples/django/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ  

この連載の最初のページ: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

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

# Step 2. Pythonパッケージのインストールの指定 - requirements.txt ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1                   # あなたの開発用ディレクトリー。任意の名前
👉      └── 📄requirements.txt
```

```plaintext
# Dockerはまだ Django 4 に対応してない？
Django>=3.0,<4.0

# PostgreSQLへ接続するためのドライバ
psycopg2>=2.8
```

# Step 3. ドッカーファイル作成 - Dockerfile ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
👉      ├── 📄Dockerfile
        └── 📄requirements.txt
```

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

# Step 4. ドッカーコンポーズファイル作成 - docker-compose.yml ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
👉      ├── 📄docker-compose.yml
        ├── 📄Dockerfile
        └── 📄requirements.txt
```

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
    command: python manage.py runserver 0.0.0.0:8000 --settings=config.settings
    #                                   ------- ---- --------------------------
    #                                   1       2    3
    # 1. Dockerコンテナ内のサーバーは localhost ではなく 0.0.0.0 と書く
    # 2. Dockerコンテナ内のWebアプリケーションのポート番号
    # 3. Djangoの設定ファイル（host1/config/settings.py）の拡張子抜き
    #                              ----------------
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

# Step 5. アプリケーション作成 - startproject 管理コマンド

あなたの開発用ディレクトリーへ移動してほしい  

```shell
cd host1
```

そして、以下のコマンドを１回だけ叩いてほしい  

```shell
docker-compose run web django-admin.py startproject webapp1 .
#                                                   -------
#                                                   任意のWebアプリケーションのフォルダー名
```

すると、あなたの開発用ディレクトリーと、その中のWebアプリケーションフォルダーの中に、以下のものが自動生成される  

```plaintext
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1
        │   ├── 📄__init__.py
        │   ├── 📄asgi.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── 📄wsgi.py
        └── 📄manage.py
```

# Step 6. 設定ファイルの移動 - settings.py ファイル

以下のファイルを移動してほしい  

```plaintext
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1
        │   ├── 📄__init__.py
        │   ├── 📄asgi.py
👉      │   ├── 📄settings.py       # これを切り取り
        │   ├── 📄urls.py
        │   └── 📄wsgi.py
        ├── 📄docker-compose.yml
        ├── 📄Dockerfile
        ├── 📄manage.py
        └── 📄requirements.txt
```

```plaintext
    └── 📂host1
        ├── 📂config                # 新規作成
👉      │   └── 📄settings.py       # ここへ移動
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1
        │   ├── 📄__init__.py
        │   ├── 📄asgi.py
        │   ├── 📄urls.py
        │   └── 📄wsgi.py
        ├── 📄docker-compose.yml
        ├── 📄Dockerfile
        ├── 📄manage.py
        └── 📄requirements.txt
```

# Step 7. 設定編集 - settings.py ファイル

続けて、そのファイルを編集してほしい  

```plaintext
    └── 📂host1
        ├── 📂config
👉      │   └── 📄settings.py
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1
        │   ├── 📄__init__.py
        │   ├── 📄asgi.py
        │   ├── 📄urls.py
        │   └── 📄wsgi.py
        ├── 📄docker-compose.yml
        ├── 📄Dockerfile
        ├── 📄manage.py
        └── 📄requirements.txt
```

```py
import os # 冒頭のあたりに追加

# ...中略...

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

# Step 8. ドッカーコンテナ起動 - docker-compose コマンド

以下のコマンドを叩いてほしい  

```shell
docker-compose up
```

# Step 9. Webページへアクセス

次に、ブラウザで以下のURLにアクセスしてほしい  

[http://localhost:8000](http://localhost:8000)  

これで、ロケットが飛んでいるページが出てくれば　インストールは完了だ。  
`[Ctrl]+[C]` キーでWebサーバーを停めることができる  

# 次の記事

📖 [Djangoでユーザー認証を付けよう！](https://qiita.com/muzudho1/items/55cb7ac55299afd51887)  
