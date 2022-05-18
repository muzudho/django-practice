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

# Step 3. 機能強化 - django-form-parser.js ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂account
            │       └── 📂v1
👉          │           └── django-form-parser.js
            └── 📂views
                └── v_account_v1.py
```

👇以下のファイルは、 django-allauth パッケージの仕様が変わったら作り直しになるかも  

```js
class DjangoFormParser {
    constructor() {

    }

    get htmlString() {
        return this._htmlString;
    }

    parseHtmlString(name, htmlString) { 
        this._htmlString = htmlString;
        console.log(`${name} htmlString=${this.htmlString}`);
        // Examples:
        // <input type="text" name="login" placeholder="Username" autocomplete="username" maxlength="150" required id="id_login">
        // <input type="password" name="password" placeholder="Password" autocomplete="current-password" required id="id_password">
        // <input type="checkbox" name="remember" id="id_remember">
        //
        // 両端の < > を外せば、 string か、 string="string" のパターンになっているが、エスケープシーケンスが入っていると難しい
        // 決め打ちをしてしまうのが簡単
        const reLogin = /<input type="text" name="login" placeholder="(.*)" autocomplete="(.*)" maxlength="(\d+)" required id="(\w+)">/;
        const rePassword = /<input type="password" name="password" placeholder="(.*)" autocomplete="(.*)" required id="(\w+)">/;
        const reRemember = /<input type="checkbox" name="remember" id="(\w+)">/;

        let groupsLogin = reLogin.exec(htmlString);
        if (groupsLogin) {
            console.log(`groupsLogin placeholder=[${groupsLogin[1]}] autocomplete=[${groupsLogin[2]}] maxlength=[${groupsLogin[3]}] id=[${groupsLogin[4]}]`)

            return {
                type: "text",
                name: "login",
                placeholder: groupsLogin[1],
                autocomplete: groupsLogin[2],
                maxlength: parseInt(groupsLogin[3]),
                id: groupsLogin[4],
            };
        }

        let groupsPassword = rePassword.exec(htmlString);
        if (groupsPassword) {
            console.log(`groupsPassword placeholder=[${groupsPassword[1]}] autocomplete=[${groupsPassword[2]}] id=[${groupsPassword[3]}]`)

            return {
                type: "password",
                name: "password",
                placeholder: groupsPassword[1],
                autocomplete: groupsPassword[2],
                id: groupsPassword[3],
            }
        }

        let groupsRemember = reRemember.exec(htmlString);
        if (groupsRemember) {
            console.log(`groupsRemember id=[${groupsRemember[1]}]`)

            return {
                type: "checkbox",
                name: "remember",
                id: groupsRemember[1],
            }
        }

        return {
            type: "undefined",
            name: "unknown",
        }
    }
}
```

# Step 4. テンプレート編集 - login.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂account
            │       └── 📂v1
            │           └── django-form-parser.js
            ├── 📂templates
            │   └── 📂account
            │       └── 📂v1
👉          │           └── 📄login.html
            └── 📂views
                └── 📄v_account_v1.py
```

👇レッスンの進み具合によって、埋め込んであるURLは 貼り替えてください  

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
                        <p>もしあなたがアカウントをまだ作っていないなら、まず <v-btn class="my-4" color="primary" :href="createPathOfSignup()">サインアップ</v-btn> してください</p>
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
                            <div class="fieldWrapper">
                                {{ form.login.errors }}
                                <v-text-field name="login" v-model="vu_userName" :maxlength="vu_loginFormDoc.maxlength" counter label="アカウント名：" required></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.password.errors }}
                                <v-text-field type="password" name="password" v-model="vu_password" counter label="パスワード：" required></v-text-field>
                            </div>
                            <div class="fieldWrapper">
                                {{ form.remember.errors }}
                                <v-checkbox v-model="vu_rememberFlag" label="パスワードを入力したままにする："></v-checkbox>
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

        <script src="{% static 'account/v1/django-form-parser.js' %}"></script>
        <!--                    ================================
                                1
            1. host1/webapp1/static/account/v1/django-form-parser.js
                                    ================================
        -->

        <script>
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印

                    // URL は、レッスンの進み具合によって適宜、貼り替えてください
                    // vu_pathOfSignin: "{% url 'account_login' %}", // django-allauth のデフォルト
                    // vu_pathOfSignin: "{% url 'account_v1_login' %}",
                    vu_pathOfSignin: "/accounts/login/", // django-allauth のログイン用パス

                    // vu_pathOfSignup: "{{ signup_url }}", // django-allauth のデフォルト
                    vu_pathOfSignup: "{% url 'account_v1_signup' %}",

                    // HTMLタグ文字列が渡されるので、解析します
                    vu_loginFormDoc: new DjangoFormParser().parseHtmlString("login", "{{ form.login|escapejs }}"),
                    vu_userName: "",

                    vu_passwordFormDoc: new DjangoFormParser().parseHtmlString("password", "{{ form.password|escapejs }}"),
                    vu_password: "",

                    vu_rememberFormDoc: new DjangoFormParser().parseHtmlString("form", "{{ form.remember|escapejs }}"),
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

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂account
            │       └── 📂v1
            │           └── django-form-parser.js
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
    path("account/v1/login/", view=v_account_v1.account_v1_login_view,
         # ----------------        ----------------------------------
         # 1                       2
         name="account_v1_login"),
    #          ----------------
    #          3
    # 1. URLの `account/v1/login/` というパスにマッチする
    # 2. 既に用意されているビューのオブジェクト？
    # 3. HTMLテンプレートの中で {% url 'account_v1_login' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/account/v1/login/](http://localhost:8000/account/v1/login/)  

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
