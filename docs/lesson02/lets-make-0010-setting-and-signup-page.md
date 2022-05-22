---
title: Djangoでユーザー認証を付けよう！
tags: Django Docker Allauth ユーザー認証
author: muzudho1
slide: false
---
# 目的

会員制サイトを作りたい。  

1. ユーザー登録（サインアップ）
2. ログイン（サインイン）
3. 指定のメールアドレスへパスワードの変更画面URLを送る機能

を付ける方法を説明する。  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
| SMTP      | smtp.gmail.com                            |
| Editor    | Visual Studio Code （以下 VSCode と表記） |
| Database  | PostgreSQL                                |

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. Gmail 側の設定をしよう

パスワードを忘れたとき、パスワード変更画面のURLがメールで飛んでくる仕掛けはよくある。  
そのメールを飛ばすサーバーは、Googleのを借りることにする。

Googleのアカウントから、

`[Googleアカウント] - [セキュリティ] - [Googleへのログイン] - [アプリパスワード]` と進んでほしい。  
アプリの名前は、例えば `DjangoPractice` とでもしておけばいいだろう。
すると 16桁の **アプリパスワード** が発行される。覚えておかなくていいと表示されるかも知れないが、一旦覚えてくれ。  

# Step 3. ".env" ファイルを作成しよう

🚫ソースにパスワードをハードコーディングしてリモートのGitリポジトリにプッシュすると被害に遭うだろう。  

パスワードのような漏れて困るものは ソースではなく 📄`.env` ファイルに書くのを習慣にし、
このファイルは 📄`.gitignore` ファイルを設定することで（あるいは既に設定してあって） リモートのGitリポジトリにプッシュしないようにしてほしい。  

```plaintext
    └── 📂host1
👉      ├── 📄.env
        └── <いろいろ>
```

```plaintext
EMAIL_HOST_USER=あなたのGmailアドレス
EMAIL_HOST_PASSWORD=あなたのGmailアドレスのアプリパスワード
```

あなたのGmailのパスワードを書くのではなく、Gmailの**アプリ**パスワードを書くという違いに気を付けてほしい。  

# Step 4. Yamlファイルの設定

以下のファイルの該当箇所を追記してほしい

```plaintext
    └── 📂host1
        ├── 📄.env
👉      ├── 🐳docker-compose.yml
        └── <いろいろ>
```

```yaml
  # Djangoアプリ
  web:
    environment:
      # 追加
      - EMAIL_HOST_USER=${EMAIL_HOST_USER}
      - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
```

意味としては `${.envファイルの中の変数名}` の内容を、 Dockerコンテナの環境変数に入れている。  
最近の Docker は、`docker-compose.yml` と同じ階層の `.env` ファイルを勝手に読み込んでくれる。  

# Step 5. requirements.txt の設定

ファイルの末尾にでも追加してほしい。  

```plaintext
    └── 📂host1
        ├── 📄.env
        ├── 🐳docker-compose.yml
👉      ├── 📄requirements.txt
        └── <いろいろ>
```

```shell
# ユーザー認証
django-allauth>=0.32.0
```

# Step 6. settings.py の設定

以下のように該当箇所を追加してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
👉      │　　├── 📄settings.py
        │　　└── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 📄requirements.txt
        └── <いろいろ>
```

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',         #追加
    'allauth',                      #追加
    'allauth.account',              #追加
    'allauth.socialaccount',        #追加
]

# ファイルの末尾にでも追加
# Allauth
# https://sinyblog.com/django/django-allauth/

SITE_ID = 1 # 動かしているサイトを識別するID
LOGIN_REDIRECT_URL = 'home' # ログオン後に遷移するURLの指定

ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/v1/login/'  # ログアウト後に遷移するURLの指定
#                              -------------------
#                              1
# 1. 例えば `http://example.com/accounts/v1/login/` というパスにマッチする
#                             -------------------

EMAIL_HOST = 'smtp.gmail.com' # メールサーバの指定
EMAIL_PORT = 587 # ポート番号の指定
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # メールサーバのGmailのアドレス
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # メールサーバのGmailのパスワード
EMAIL_USE_TLS = True # TLSの設定（TRUE,FALSE)
```

# Step 7. Docker コンテナの再起動 - コマンド実行

Dockerコンテナは起動しているものとし、以下のコマンドを打鍵してほしい。  

```shell
docker-compose down
```

Dockerコンテナは停止しているものとし、以下のコマンドを打鍵してほしい。  

```shell
docker-compose build

docker-compose run --rm web python3 manage.py makemigrations

docker-compose run --rm web python3 manage.py migrate

docker-compose up
```

# Step 8. urls.py の設定

以下のように該当箇所を追加してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │　　├── 📄settings.py
👉      │　　├── 📄urls.py
        │　　└── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 📄requirements.txt
        └── <いろいろ>
```

```py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from webapp1.views import v_accounts_v1
#    ------- -----        -------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # 管理画面
    path('admin/', admin.site.urls),
    #     ------   ---------------
    #     1        2
    # 1. 例えば `http://example.com/admin/` のような URLのパスの部分
    # 2. django に用意されている管理画面のパスを 1. のパスにぶら下げる形で全てコピーします




    # +----
    # | Allauth
    # | See also: https://sinyblog.com/django/django-allauth/

    # ログイン後に戻ってくるWebページの指定
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #    --  -----------------------------------------------        ----
    #    1   2                                                      3
    # 1. URL に パスを付けなかったときにマッチする
    # 2. 最初から用意されているページ？
    # 3. ログイン後に飛んでくるページの URL のパスを 'home' という名前で覚えておく

    # allauth の URLのパスのコピー
    path('accounts/v1/', include('allauth.urls')),
    #     ------------   -----------------------
    #     1
    # 1. 例えば `http://example.com/accounts/v1/` のような URLのパスの部分
    # 2. allauth の例えば `login/` のようなパスを 1. のパスにぶら下げる形で全てコピーします

    # | Allauth
    # +----
]
```


# Step 9. Webページへアクセス

📖 [http://localhost:8000/accounts/v1/login/](http://localhost:8000/accounts/v1/login/)  

あとは アカウントを作成したり、パスワードを忘れたときの手続きを試してほしい。  

# 次の記事

📖 [DjangoでWebページを追加しよう！](https://qiita.com/muzudho1/items/06fe071c1147b4b8f062)  
* もっと勉強したい人向けの関連記事
  * 📚 [Djangoで、django-allauthのテンプレートを差し替えよう！](https://qiita.com/muzudho1/items/6120055b2a8eb4e28527)

# 参考にした記事

📖 [爆速で作れるDjangoユーザ認証機能【django-allauth】](https://sinyblog.com/django/django-allauth/)  
📖 [Django 認証機能がうまく反映されない](https://qiita.com/cardene/items/00fc55a6ba4915cf83e9)  
📖 [django-allauth Installation](https://django-allauth.readthedocs.io/en/latest/installation.html)  
📖 [docker-compose.ymlで.envファイルに定義した環境変数を使う](https://kitigai.hatenablog.com/entry/2019/05/08/003000)  
📖 [Redmineにて、メールのgmail（2段階認証設定）に送付するときに行った対処法](https://zenn.dev/gashi/articles/67e6c244942ef1318395)  
📖 [【Django】認証したユーザー（super, staff, active）の権限でアクセス制限・表示制限を設定する](https://office54.net/python/django/django-access-limit)  
