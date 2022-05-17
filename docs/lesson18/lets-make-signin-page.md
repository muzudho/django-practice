# 目的

見た目がマシな　サインイン（利用開始）のページがほしい。  

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
        │   │   └── 📄mh_session.py
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
        │   │   └── 📂tic-tac-toe
        │   │       ├── 📂v1
        │   │       │   └── 📄<いろいろ>
        │   │       ├── 📂v2
        │   │       │   ├── 📄match_request.html
        │   │       │   └── 📄play.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   ├── 📄v_tic_tac_toe_v1.py
        │   │   ├── 📄v_tic_tac_toe_v2.py
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       │   └── 📄consumer.py
        │   │       └── 📂v2
        │   │           ├── 📄consumer.py
        │   │           └── 📄protocol.py
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

# Step 2. ビュー編集 - v_account_v1.py ファイル

以下のファイルを 無ければ新規作成、有れば編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
👉              └── v_account_v1.py
```

```py
# See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
from allauth.account.views import SignupView, LoginView

# ...中略...

class AccountV1LoginView(LoginView):
    """django-allauth のログイン ビューを継承します
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)
    """

    # ファイルパス
    template_name = "account/v1/login.html"
    #                ------------------------
    #                1
    # 1. host1/webapp1/templates/account/v1/login.html を取得
    #                            ---------------------


# グローバル変数
account_v1_login_view = AccountV1LoginView.as_view()
```

# Step 3. テンプレート編集 - login.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂account
            │       └── 📂v1
👉          │           └── 📄login.html
            └── 📂views
                └── 📄v_account_v1.py
```

```html
<!--
    📖[login.html](https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/login.html)
-->
<!-- extends "account/base.html" -->
<!-- -->
{% load i18n %}

<!-- -->
{% load account socialaccount %}

<!-- -->
{% block head_title %}{% trans "Sign In" %}{% endblock %}

<!-- -->
{% block content %}

<!-- -->
<h1>{% trans "Sign In" %}</h1>

<!-- -->
{% get_providers as socialaccount_providers %}

<!-- -->
{% if socialaccount_providers %}
<p>{% blocktrans with site.name as site_name %}Please sign in with one of your existing third party accounts. Or, <a href="{{ signup_url }}">sign up</a> for a {{ site_name }} account and sign in below:{% endblocktrans %}</p>

<div class="socialaccount_ballot">
    <ul class="socialaccount_providers">
        <!-- -->
        {% include "socialaccount/snippets/provider_list.html" with process="login" %}
        <!-- -->
    </ul>

    <div class="login-or">{% trans 'or' %}</div>
</div>

<!-- -->
{% include "socialaccount/snippets/login_extra.html" %}
<!-- -->

<!-- -->
{% else %}
<!-- -->
<p>{% blocktrans %}If you have not created an account yet, then please <a href="{{ signup_url }}">sign up</a> first.{% endblocktrans %}</p>
<!-- -->
{% endif %}
<!-- -->

<form class="login" method="POST" action="{% url 'account_login' %}">
    <!-- -->
    {% csrf_token %}
    <!-- -->
    {{ form.as_p }}
    <!-- -->
    {% if redirect_field_value %}
    <!-- -->
    <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
    <!-- -->
    {% endif %}
    <!-- -->
    <a class="button secondaryAction" href="{% url 'account_reset_password' %}">{% trans "Forgot Password?" %}</a>
    <button class="primaryAction" type="submit">{% trans "Sign In" %}</button>
</form>

<!-- -->
{% endblock %}
<!-- -->
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂account
            │       └── 📂v1
            │           └── 📄login.html
            ├── 📂views
            │   └── 📄v_account_v1.py
👉          └── 📄urls.py
```

```py
from django.urls import include, path

from webapp1.views import v_account_v1
#    ------- -----        ------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # サインイン
    path("account/v1/login/", view=v_account_v1.account_v1_login_view),
    #     -----------------        ----------------------------------
    #     1                         2
    # 1. URLの `account/v1/login/` というパスにマッチする
    # 2. 既に用意されているビューのオブジェクト？
]
```

# Step 5. Web画面へアクセス

📖 [http://localhost:8000/account/v1/login/](http://localhost:8000/account/v1/login/)  
