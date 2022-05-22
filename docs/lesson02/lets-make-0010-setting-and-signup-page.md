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
        ├── 📂webapp1                       # アプリケーション フォルダー
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

# ... 中略 ...

# 調べ終わったら消す
# Example: `/code/webapp1/templates`
#print(
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

# ... 中略 ...

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

# Step 8. 機能強化 - form-html-parser.js ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂static
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
👉      │   │           └── 📄form-html-parser.js
        │　　├── 📄settings.py
        │　　└── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 📄requirements.txt
        └── <いろいろ>
```

👇以下のファイルは、 django-allauth パッケージのHTML出力の仕様が変わったら作り直してください  

```js
class DjangoAllauthFormParser {
    constructor() {

    }

    get htmlString() {
        return this._htmlString;
    }

    parseHtmlString(name, htmlString) { 
        this._htmlString = htmlString;
        console.log(`${name} htmlString=${this.htmlString}`);
        // Examples:
        //
        // signup.html
        // <input type="text" name="username" placeholder="Username" autocomplete="username" minlength="1" maxlength="150" required id="id_username">
        // <label for="id_email">E-mail (optional):</label></th><td><input type="email" name="email" placeholder="E-mail address" autocomplete="email" id="id_email">
        // <label for="id_password1">Password:</label></th><td><input type="password" name="password1" placeholder="Password" autocomplete="new-password" required id="id_password1">
        // <label for="id_password2">Password (again):</label></th><td><input type="password" name="password2" placeholder="Password (again)" autocomplete="new-password" required id="id_password2">
        //
        // login.html
        // <input type="text" name="login" placeholder="Username" autocomplete="username" maxlength="150" required id="id_login">
        // <input type="password" name="password" placeholder="Password" autocomplete="current-password" required id="id_password">
        // <input type="checkbox" name="remember" id="id_remember">
        //
        // 両端の < > を外せば、 string か、 string="string" のパターンになっているが、エスケープシーケンスが入っていると難しい
        // 決め打ちをしてしまうのが簡単

        // signup.html
        const reUsername = /<input type="text" name="username" placeholder="(.*)" autocomplete="(.*)" minlength="(\d+)" maxlength="(\d+)" required id="(\w+)">/;
        const reEmail = /<input type="email" name="email" placeholder="(.*)" autocomplete="(.*)" id="(\w+)">/;
        const rePassword1 = /<input type="password" name="password1" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;
        const rePassword2 = /<input type="password" name="password2" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;

        // login.html
        const reLogin = /<input type="text" name="login" placeholder="(.*)" autocomplete="(.*)" maxlength="(\d+)" required id="(\w+)">/;
        const rePassword = /<input type="password" name="password" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;
        const reRemember = /<input type="checkbox" name="remember" id="(\w+)">/;

        // signup.html username
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`username placeholder=[${groups[1]}] autocomplete=[${groups[2]}] minlength=[${groups[3]}] maxlength=[${groups[4]}] id=[${groups[5]}]`)

                return {
                    type: "text",
                    name: "username",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    minlength: parseInt(groups[3]),
                    maxlength: parseInt(groups[4]),
                    id: groups[5],
                };
            }
        }

        // signup.html email
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`email placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "email",
                    name: "email",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                };
            }
        }

        // signup.html password1
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`password1 placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "password",
                    name: "password1",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                };
            }
        }

        // signup.html password2
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`password2 placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "password",
                    name: "password2",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                };
            }
        }

        // login.html login
        {
            let groups = reLogin.exec(htmlString);
            if (groups) {
                console.log(`login placeholder=[${groups[1]}] autocomplete=[${groups[2]}] maxlength=[${groups[3]}] id=[${groups[4]}]`)

                return {
                    type: "text",
                    name: "login",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    maxlength: parseInt(groups[3]),
                    id: groups[4],
                };
            }
        }

        // login.html password
        {
            let groups = rePassword.exec(htmlString);
            if (groups) {
                console.log(`password placeholder=[${groups[1]}] autocomplete=[${groups[2]}] id=[${groups[3]}]`)

                return {
                    type: "password",
                    name: "password",
                    placeholder: groups[1],
                    autocomplete: groups[2],
                    id: groups[3],
                }
            }
        }

        // login.html remember
        {
            let groups = reRemember.exec(htmlString);
            if (groups) {
                console.log(`remember id=[${groups[1]}]`)

                return {
                    type: "checkbox",
                    name: "remember",
                    id: groups[1],
                }
            }
        }

        return {
            type: "undefined",
            name: "unknown",
        }
    }
}
```

# Step 9. テンプレート編集 - signup.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂static
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
        │   │           └── 📄form-html-parser.js
        │   ├── 📂templates
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
👉      │   │           └── 📄signup.html
        │　　├── 📄settings.py
        │　　└── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 📄requirements.txt
        └── <いろいろ>
```

👇レッスンの進み具合によって、埋め込んであるURLは 貼り替えてください  

```html
<!--
    # See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
-->
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!-- -->
<!DOCTYPE html>
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>サインアップ</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <!-- v-app-bar に app プロパティを指定しないなら、背景画像を付けてほしい -->
                <v-app-bar app dense elevation="4">
                    <v-app-bar-nav-icon></v-app-bar-nav-icon>
                    <v-toolbar-title>サインアップ</v-toolbar-title>
                </v-app-bar>
                <v-main>
                    <v-container>
                        <h3>既にアカウントを持っているなら</h3>
                        <v-btn class="my-4" color="primary" :href="createPathOfSignin()">サインイン</v-btn>
                    </v-container>
                    <v-container>
                        <h3>会員登録するなら</h3>
                        <form class="signup" id="signup_form" method="post" :action="createPathOfSignup()">
                            <!-- -->
                            {% csrf_token %}
                            <!-- -->
                            <!-- 手動フォーム作成 ここから -->
                            {{ form.non_field_errors }}
                            <div class="fieldWrapper">
                                {{ form.username.errors }}
                                <v-text-field name="username" v-model="vu_userName" :minlength="vu_usernameFormDoc.minlength" :maxlength="vu_usernameFormDoc.maxlength" counter label="ユーザー名：" required></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.email.errors }}
                                <v-text-field name="email" v-model="vu_email" counter label="E-mali："></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.password1.errors }}
                                <v-text-field type="password" name="password1" v-model="vu_password1" counter label="パスワード：" required></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.password2.errors }}
                                <v-text-field type="password" name="password2" v-model="vu_password2" counter label="パスワード（再入力）：" required></v-text-field>
                            </div>
                            <!-- 手動フォーム作成 ここまで -->
                            {% if redirect_field_value %}
                            <!-- -->
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
                            <!-- -->
                            {% endif %}
                            <!-- -->
                            <v-btn class="my-4" color="primary" type="submit">サインアップ &raquo;</v-btn>
                        </form>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>

        <script src="{% static 'allauth-customized/v1/form-html-parser.js' %}"></script>
        <!--                    =========================================
                                1
            1. host1/webapp1/static/allauth-customized/v1/form-html-parser.js
                                    =========================================
        -->

        <script>
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印

                    // URL は、レッスンの進み具合によって適宜、貼り替えてください
                    // vu_pathOfSignin: "{{ login_url }}", // django-allauth のデフォルト
                    vu_pathOfSignin: "{% url 'accounts_v1_login' %}",

                    // vu_pathOfSignup: "{% url 'accounts_v1_signup' %}",
                    vu_pathOfSignup: "{% url 'account_signup' %}", // django-allauth のサインアップ用パス

                    // HTMLタグ文字列が渡されるので、解析します
                    vu_usernameFormDoc: new DjangoAllauthFormParser().parseHtmlString("username", "{{ form.username|escapejs }}"),
                    vu_userName: "",

                    vu_emailFormDoc: new DjangoAllauthFormParser().parseHtmlString("email", "{{ form.email|escapejs }}"),
                    vu_email: "",

                    vu_password1FormDoc: new DjangoAllauthFormParser().parseHtmlString("password1", "{{ form.password1|escapejs }}"),
                    vu_password1: "",

                    vu_password2FormDoc: new DjangoAllauthFormParser().parseHtmlString("password2", "{{ form.password2|escapejs }}"),
                    vu_password2: "",
                },
                methods: {
                    createPathOfSignin() {
                        let path = `${location.protocol}//${location.host}${this.vu_pathOfSignin}`;
                        //          --------------------  ---------------]-----------------------
                        //          1                     2               3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`SignIn path=[${path}]`);
                        return path;
                    },
                    createPathOfSignup() {
                        let path = `${location.protocol}//${location.host}${this.vu_pathOfSignup}`;
                        //          --------------------  ---------------]-----------------------
                        //          1                     2               3
                        // 1. protocol
                        // 2. host
                        // 3. path
                        console.log(`SignUp path=[${path}]`);
                        return path;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 10. ビュー編集 - v_accounts_v1.py ファイル

以下のファイルを 無ければ新規作成、有れば編集してほしい  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂static
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
        │   │           └── 📄form-html-parser.js
        │   ├── 📂templates
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
        │   │           └── 📄signup.html
        │   ├── 📂views
👉      │   │   └── v_accounts_v1.py
        │　　├── 📄settings.py
        │　　└── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 📄requirements.txt
        └── <いろいろ>
```

```py
# See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
from allauth.account.views import SignupView


class AccountsV1SignupView(SignupView):
    """django-allauth のサインアップ ビューを継承します
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/views.py)
    """

    # ファイルパス
    template_name = "allauth-customized/v1/account/signup.html"
    #                -----------------------------------------
    #                1
    # 1. host1/webapp1/templates/allauth-customized/v1/account/signup.html を取得
    #                            -----------------------------------------

    # You can also override some other methods of SignupView
    # Like below:
    # def form_valid(self, form):
    #     ...
    #
    # def get_context_data(self, **kwargs):
    #     ...


# グローバル変数
accounts_v1_signup_view = AccountsV1SignupView.as_view()
```

# Step 11. urls.py の設定

以下のように該当箇所を追加してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂static
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
        │   │           └── 📄form-html-parser.js
        │   ├── 📂templates
        │   │   └── 📂allauth-customized
        │   │       └── 📂v1
        │   │           └── 📄signup.html
        │   ├── 📂views
        │   │   └── v_accounts_v1.py
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

    # サインアップ（会員登録）
    path("accounts/v1/signup/", view=v_accounts_v1.accounts_v1_signup_view,
         # ------------------        -------------------------------------
         # 1                        2
         name="accounts_v1_signup"),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/accounts/v1/signup/` のような URL のパスの部分にマッチする
    #                              -------------------
    # 2. allauth の SignupView をカスタマイズしたオブジェクト
    # 3. HTMLテンプレートの中で {% url 'accounts_v1_signup' %} のような形でURLを取得するのに使える

    # | Allauth
    # +----
]
```


# Step 12. Webページへアクセス

📖 [http://localhost:8000/accounts/v1/signup/](http://localhost:8000/accounts/v1/signup/)  

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

## 認証関連

📖 [pennersr / django-allauth](https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/signup.html) - テンプレートの原型   
📖 [django-allauth Templates](https://django-allauth.readthedocs.io/en/latest/templates.html)  
📖 [Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)  
📖 [【Django】django-allauthのformやhtmlを上書きする方法](https://qiita.com/NOIZE/items/0522825a1de1d6aa4a2b)  
📖 [【Django】認証のViewをカスタマイズする方法 テンプレート編](https://allneko.club/django/auth-views-customize/)  

## form関連

📖 [Working with forms](https://docs.djangoproject.com/en/4.0/topics/forms/) - 一番詳しい  
📖 [forms.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py) - 原型  
📖 [How can I render Django Form with vuetify?](https://stackoverflow.com/questions/63993890/how-can-i-render-django-form-with-vuetify)  
📖 [vue.js - Vuetifyの入力値でDjangoのテンプレートタグを使用する方法は？](https://tutorialmore.com/questions-2757963.htm)  
📖 [Anyone know how to use vuetify with django form?](https://forum.djangoproject.com/t/anyone-know-how-to-use-vuetify-with-django-form/4807)  
📖 [Source code for django.forms.boundfield](https://docs.djangoproject.com/en/2.2/_modules/django/forms/boundfield/)  
📖 [DjangoのFormクラスを使う](https://qiita.com/taumu/items/4587a91c4d7d2db165b3)  
