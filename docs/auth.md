# ユーザー認証ページを作るには？

📖 [爆速で作れるDjangoユーザ認証機能【django-allauth】](https://sinyblog.com/django/django-allauth/)  
📖 [Django 認証機能がうまく反映されない](https://qiita.com/cardene/items/00fc55a6ba4915cf83e9)  
📖 [django-allauth Installation](https://django-allauth.readthedocs.io/en/latest/installation.html)  
📖 [docker-compose.ymlで.envファイルに定義した環境変数を使う](https://kitigai.hatenablog.com/entry/2019/05/08/003000)  
📖 [Redmineにて、メールのgmail（2段階認証設定）に送付するときに行った対処法](https://zenn.dev/gashi/articles/67e6c244942ef1318395)  

## Gmail の設定1

Gmailのパスワードが漏洩してはいけないので、以下の方法でアプリケーションのために特別なパスワードを作成します。

`[Googleアカウント] - [セキュリティ] - [Googleへのログイン] - [アプリパスワード]` と進んでください。  

アプリの名前を入力（例えば `DjangoPractice`）するとパスワードが発行されます。これを一旦覚えておいてください。  

## Gmail の設定2

以下のファイルを新規作成してください  

📄host1/.env

```plaintext
EMAIL_HOST_USER=あなたのGmailアドレス
EMAIL_HOST_PASSWORD=あなたのGmailアドレスのアプリパスワード
```

👆 🚫上記の .env ファイルにはパスワードを含むため、誤って GitHub にアップロードをするといったことのないようにしてください

# ファイルの設定

以下のファイルの該当箇所を編集してください

📄host1/docker-compose.yml

```yaml
  # Djangoアプリ
  web:
    environment:
      # 追加
      - EMAIL_HOST_USER=${EMAIL_HOST_USER}
      - EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
```

```shell
# pip install django-allauth
```

📄host1/requirements.txt

```shell
# 追加
# ユーザー認証
django-allauth>=0.32.0
```

コマンドの打鍵

```shell
# python manage.py startapp accounts
```

📄host1/webapp1/settings.py:  

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
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/' # ログアウト後に遷移するURLの指定
 
EMAIL_HOST = 'smtp.gmail.com' # メールサーバの指定
EMAIL_PORT = 587 # ポート番号の指定
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # メールサーバのGmailのアドレス
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # メールサーバのGmailのパスワード
EMAIL_USE_TLS = True # TLSの設定（TRUE,FALSE)
```

📄host1/webapp1/urls.py の編集

```py
from django.contrib import admin
from django.urls import include, path #includeを追加
from django.views.generic import TemplateView #追加
 
urlpatterns = [
    path('admin/', admin.site.urls),

    # Allauth
    # See also: https://sinyblog.com/django/django-allauth/
    path('', TemplateView.as_view(template_name='home.html'), name='home'), #追加。ログオン後のTOP画面の定義
    path('accounts/', include('allauth.urls')), #追加
]
```

以下のコマンドを打鍵してください  

```shell
docker-compose build

docker-compose run --rm web python3 manage.py makemigrations

docker-compose run --rm web python3 manage.py migrate

docker-compose up
```

* http://localhost:8000/accounts/login/
* [Ctrl]+[C]キーで停止

# Documents

📖 [Djangoでユーザー認証を付けよう！](https://qiita.com/muzudho1/items/55cb7ac55299afd51887)  
