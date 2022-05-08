# 目的

環境を用意する。  

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

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

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
    └── 📂host1
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

📖 [Djangoでユーザー認証を付けよう！](https://qiita.com/muzudho1/items/55cb7ac55299afd51887)  
