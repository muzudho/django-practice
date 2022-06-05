"""
Django settings for webapp1 project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zi^6=@s652)x3roh+^2c+f8mx*oap#em#)l%(#i*b+e5hei$dq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# さくらVPSを借りたりしたときは、ここにホストを設定すると 外からアクセスできる
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'webapp1',  # 追加
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 追加 allauth
    'django.contrib.sites',  # 追加
    'allauth',  # 追加
    'allauth.account',  # 追加
    'allauth.socialaccount',  # 追加

    # （追加） For web socket
    'channels',

    # （追加） For gRPC
    'django_grpc_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp1.urls'

# 調べ終わったら消す
# Example: `/code/webapp1/templates`
# print(
#    f"os.path.join(BASE_DIR, 'webapp1', 'templates')={os.path.join(BASE_DIR, 'webapp1', 'templates')}")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # +----
            # | My project templates

            # 'DIRS' 配列には全く指定しないか、１つでも指定するなら デフォルトのテンプレート フォルダーを含めるようにしてください
            os.path.join(BASE_DIR, 'webapp1', 'templates', 'webapp1'),
            #            --------   -------    ---------    -------
            #            1          2          3            4
            # 1. 開発環境によってパスが変わることに注意してください。 2. 3. も適宜 設定してください
            # 2. 自アプリケーション フォルダー
            # 3. テンプレート フォルダー
            # 4. 自アプリケーション フォルダーと同名のフォルダー。 他のアプリケーションのテンプレートと共存したい場合に置いてください
            #
            # Example: /code/webapp1/templates/webapp1
            #          ----- ------- --------- -------
            #          1     2       3         4

            # | My project templates
            # +----

            # +----
            # | allauth

            os.path.join(BASE_DIR, 'webapp1', 'templates',
                         # ------   -------    ---------
                         # 1        2          3
                         'allauth-customized', 'v1'),
            #             -------------------------
            #             4
            # 1. 開発環境によってパスが変わることに注意してください。 2. 3. も適宜 設定してください
            # 2. 自アプリケーション フォルダー
            # 3. テンプレート フォルダー
            # 4. 別アプリケーションのフォルダー名、また任意でバージョン番号フォルダー
            #
            # Example: /code/webapp1/templates/allauth-customized/v1
            #          ----- ------- --------- ---------------------
            #          1     2       3         4

            # | allauth
            # +----
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# （削除） WSGI_APPLICATION = 'webapp1.wsgi.application'
ASGI_APPLICATION = "webapp1.asgi.application"
#                   -------
#                   1
# 1. アプリケーション フォルダー名

# （追加） See also: 📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
CHANNEL_LAYERS = {
    'default': {
        # Method 1: Via redis lab
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [
        #       'redis://h:<password>;@<redis Endpoint>:<port>'
        #     ],
        # },

        # Method 2: Via local Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #      "hosts": [('127.0.0.1', 6379)],
        # },

        # Method 3: Via In-memory channel layer
        # Using this method.
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }
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

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth
# https://sinyblog.com/django/django-allauth/

SITE_ID = 1  # 動かしているサイトを識別するID

# ログインしていないときに飛ばされる先。指定しないと '/accounts/login/'
LOGIN_URL = '/accounts/v1/login/'  # 慣れない内は URL で指定
# LOGIN_URL = 'login' # 慣れてくれば name で指定

# LOGIN_REDIRECT_URL = 'home'  # ログイン後に遷移するURLの指定
LOGIN_REDIRECT_URL = 'homeV1_home'  # ログイン後に遷移するURLの指定

# ログアウト後に遷移するURLの指定
#
# * レッスンの進捗に応じて変えてください
#
# ACCOUNT_LOGOUT_REDIRECT_URL = 'home' # レッスンの最初はこれ
# ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/v1/login/'
#                              -------------------
#                              1
# 1. 例えば `http://example.com/accounts/v1/login/` というパスにマッチする
#                             -------------------
ACCOUNT_LOGOUT_REDIRECT_URL = 'homeV1_home'

EMAIL_HOST = 'smtp.gmail.com'  # メールサーバの指定
EMAIL_PORT = 587  # ポート番号の指定
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # メールサーバのGmailのアドレス
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # メールサーバのGmailのパスワード
EMAIL_USE_TLS = True  # TLSの設定（TRUE,FALSE)
