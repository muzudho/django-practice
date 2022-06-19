# 目的

見た目がマシな　サインイン（利用開始）のページがほしい  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている  

```plaintext
    └── 📂host1                   # あなたの開発用ディレクトリー。任意の名前
        ├── 📂config
        │   └── 📄settings.py
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
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
        │   ├── 📄__init__.py
        │   ├── 📄asgi.py
        │   ├── 📄urls.py
        │   └── 📄wsgi.py
        ├── 📄.env
        ├── 📄docker-compose.yml
        ├── 📄Dockerfile
        ├── 📄manage.py
        └── 📄requirements.txt
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. テンプレート作成 - login.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1                   # あなたの開発用ディレクトリー。任意の名前
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂allauth-customized
                    └── 📂v1
                        └── 📂account           # allauth のディレクトリー構成を真似ます
👉                          └── 📄login.html
```

👇レッスンの進み具合によって、埋め込んであるURLは 貼り替えてほしい  

```html
<!--
    📖[login.html](https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/login.html)
-->

<!--
    # See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
-->
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!-- -->
{% load i18n %}
<!-- -->
{% load account socialaccount %}
<!-- -->
{% get_providers as socialaccount_providers %}
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
        <title>サインイン</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <!-- v-app-bar に app プロパティを指定しないなら、背景画像を付けてほしい -->
                <v-app-bar app dense elevation="4">
                    <v-app-bar-nav-icon></v-app-bar-nav-icon>
                    <v-toolbar-title>サインイン</v-toolbar-title>
                </v-app-bar>
                <v-main>
                    <v-container>
                        <h3>もし会員登録をしてないなら</h3>
                        {% if socialaccount_providers %}

                        <!-- 👇ここらへん分からない -->
                        <p>{% blocktrans with site.name as site_name %}Please sign in with one of your existing third party accounts. Or, <a href="{{ signup_url }}">sign up</a> for a {{ site_name }} account and sign in below:{% endblocktrans %}</p>
                        <div class="socialaccount_ballot">
                            <ul class="socialaccount_providers">
                                <!-- -->
                                {% include "socialaccount/snippets/provider_list.html" with process="login" %}
                                <!-- -->
                            </ul>

                            <div class="login-or">or</div>
                        </div>
                        <!-- -->
                        {% include "socialaccount/snippets/login_extra.html" %}
                        <!-- 👆ここらへん分からない -->

                        <!-- -->
                        {% else %}
                        <!-- 👇こっちが出てくる -->
                        <p>もし　あなたがアカウントを　まだ作っていないなら、まず <v-btn class="my-4" color="primary" :href="createPathOfSignup()">サインアップ</v-btn> してください</p>
                        <!-- 👆こっちが出てくる -->
                        {% endif %}
                        <!-- -->
                    </v-container>
                    <v-container>
                        <h3>サインイン（利用開始）</h3>
                        <form class="login" method="POST" :action="createPathOfSignin()">
                            <!-- -->
                            {% csrf_token %}
                            <!-- 手動フォーム作成 ここから -->
                            {{ form.non_field_errors }}
                            <!-- ユーザー名 -->
                            <div class="fieldWrapper">
                                {{ form.login.errors }}
                                <v-text-field name="login" v-model="vu_userName.value" :rules="vu_userName.rules" counter="16" label="ユーザー名" required hint="使える文字 a-z， 0-9． 先頭に数字は使えません。 最大 16 文字"></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.password.errors }}
                                <v-text-field type="password" name="password" v-model="vu_password" counter label="パスワード" required></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.remember.errors }}
                                <v-checkbox v-model="vu_rememberFlag" label="パスワードを入力したままにする"></v-checkbox>
                            </div>
                            <!-- 手動フォーム作成 ここまで -->
                            <!-- -->
                            {% if redirect_field_value %}
                            <!-- -->
                            <input type="hidden" name="{{ redirect_field_name }}" value="{{ redirect_field_value }}" />
                            <!-- -->
                            {% endif %}
                            <!-- -->
                            <v-btn class="my-4" color="primary" type="submit">サインイン</v-btn>
                            <a class="button secondaryAction" href="{% url 'account_reset_password' %}">パスワードを忘れたら</a>
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
                    // vu_pathOfSignin: "{% url 'account_login' %}", // django-allauth のデフォルト
                    // vu_pathOfSignin: "{% url 'accounts_v1_login' %}",
                    vu_pathOfSignin: "/accounts/v1/login/", // urls.py で設定した django-allauth のログイン用パス

                    // vu_pathOfSignup: "{{ signup_url }}", // django-allauth のデフォルト
                    vu_pathOfSignup: "{% url 'accounts_v1_signup' %}",

                    // HTMLタグ文字列が渡されるので、解析します
                    vu_loginFormDoc: new DjangoAllauthFormParser().parseHtmlString("login", "{{ form.login|escapejs }}"),

                    // ユーザー名
                    vu_userName: {
                        value: "",
                        rules: [
                            // FIXME ここでルールを色々書いているが、モデル側で対応していないので、モデル側も対応してほしい
                            (value) => !!value || "Required", // 空欄の禁止
                            (v) => v.length <= 16 || "Max 16 characters", // 文字数上限
                            (value) => {
                                const pattern = /^[a-z][a-z0-9]*$/; // 正規表現で指定
                                return pattern.test(value) || "Invalid format";
                            },
                        ],
                    },

                    vu_passwordFormDoc: new DjangoAllauthFormParser().parseHtmlString("password", "{{ form.password|escapejs }}"),
                    vu_password: "",

                    vu_rememberFormDoc: new DjangoAllauthFormParser().parseHtmlString("form", "{{ form.remember|escapejs }}"),
                    vu_rememberFlag: false,
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

# Step 3. ビュー編集 - v_accounts_v1.py ファイル

以下のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂allauth-customized
            │       └── 📂v1
            │           └── 📂account
            │               └── 📄login.html
            └── 📂views
👉              └── v_accounts_v1.py
```

```py
# See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
from allauth.account.views import LoginView

# ...中略...

class AccountsV1LoginView(LoginView):
    """django-allauth のログイン ビューをカスタマイズします
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)
    """

    # ファイルパス
    template_name = "allauth-customized/v1/account/login.html"
    #                ----------------------------------------
    #                1
    # 1. host1/webapp1/templates/allauth-customized/v1/account/login.html を取得
    #                            ----------------------------------------


# グローバル変数
accounts_v1_login_view = AccountsV1LoginView.as_view()
```

# Step 4. ルート編集 - urls.py ファイル

以下の既存ファイルに、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂allauth-customized
            │       └── 📂v1
            │           └── 📂account
            │               └── 📄login.html
            ├── 📂views
            │   └── 📄v_account_v1.py
👉          └── 📄urls.py
```

```py
from django.urls import include, path

from webapp1.views import v_accounts_v1
#    ------- -----        -------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # サインイン
    path("account/v1/login/", view=v_accounts_v1.accounts_v1_login_view,
         # ----------------        ------------------------------------
         # 1                       2
         name="accounts_v1_login"),
    #          -----------------
    #          3
    # 1. URLの `account/v1/login/` というパスにマッチする
    # 2. 既に用意されているビューのオブジェクト？
    # 3. HTMLテンプレートの中で {% url 'accounts_v1_login' %} のような形でURLを取得するのに使える
]
```

# Step 5. Web画面へアクセス

📖 [http://localhost:8000/accounts/v1/login/](http://localhost:8000/accounts/v1/login/)  

👆 ログイン ページを開く  

既にログインしているなら、  

📖 [http://localhost:8000/accounts/v1/logout/](http://localhost:8000/accounts/v1/logout/)  

👆 ログアウトを試してほしい  

# 次の記事

📖 [Djangoでポータルページを作成しよう！](https://qiita.com/muzudho1/items/ad2299cf94a9a5b1c254)  

# 関連する記事

📖 [login.html](https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/login.html) - テンプレートの原型  

## form関連

📖 [Working with forms](https://docs.djangoproject.com/en/4.0/topics/forms/) - 一番詳しい  
📖 [forms.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py) - 原型  
📖 [How can I render Django Form with vuetify?](https://stackoverflow.com/questions/63993890/how-can-i-render-django-form-with-vuetify)  
📖 [vue.js - Vuetifyの入力値でDjangoのテンプレートタグを使用する方法は？](https://tutorialmore.com/questions-2757963.htm)  
📖 [Anyone know how to use vuetify with django form?](https://forum.djangoproject.com/t/anyone-know-how-to-use-vuetify-with-django-form/4807)  
📖 [Source code for django.forms.boundfield](https://docs.djangoproject.com/en/2.2/_modules/django/forms/boundfield/)  
📖 [DjangoのFormクラスを使う](https://qiita.com/taumu/items/4587a91c4d7d2db165b3)  
