# 目的

見た目がマシな　サインアップ（会員登録）のページがほしい。  

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
from allauth.account.views import SignupView


class AccountV1SignupView(SignupView):
    """django-allauth のサインアップ ビューを継承します"""

    # ファイルパス
    template_name = "account/v1/signup.html"
    #                ------------------------
    #                1
    # 1. host1/webapp1/templates/account/v1/signup.html を取得
    #                            ----------------------

    # You can also override some other methods of SignupView
    # Like below:
    # def form_valid(self, form):
    #     ...
    #
    # def get_context_data(self, **kwargs):
    #     ...


# グローバル変数
account_v1_signup_view = AccountV1SignupView.as_view()
```

# Step 3. 機能強化 - django-allauth-form-parser.js ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂account
            │       └── 📂v1
👉          │           └── django-allauth-form-parser.js
            └── 📂views
                └── v_account_v1.py
```

👇以下のファイルは、 django-allauth パッケージの仕様が変わったら作り直しになるかも  

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

# Step 4. テンプレート編集 - signup.html ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂account
            │       └── 📂v1
            │           └── django-allauth-form-parser.js
            ├── 📂templates
            │   └── 📂account
            │       └── 📂v1
👉          │           └── 📄signup.html
            └── 📂views
                └── 📄v_account_v1.py
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

        <script src="{% static 'account/v1/django-allauth-form-parser.js' %}"></script>
        <!--                    ========================================
                                1
            1. host1/webapp1/static/account/v1/django-allauth-form-parser.js
                                    ========================================
        -->

        <script>
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印

                    // URL は、レッスンの進み具合によって適宜、貼り替えてください
                    // vu_pathOfSignin: "{{ login_url }}", // django-allauth のデフォルト
                    vu_pathOfSignin: "{% url 'account_v1_login' %}",

                    // vu_pathOfSignup: "{% url 'account_v1_signup' %}",
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

# Step 5. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   └── 📂account
            │       └── 📂v1
            │           └── django-allauth-form-parser.js
            ├── 📂templates
            │   └── 📂account
            │       └── 📂v1
            │           └── 📄signup.html
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

    # サインアップ
    path("account/v1/signup/", view=v_account_v1.account_v1_signup_view,
         # -----------------        -----------------------------------
         # 1                        2
         name="account_v1_signup"),
    #          ------------------
    #          3
    # 1. URLの `account/v1/signup/` というパスにマッチする
    # 2. 既に用意されているビューのオブジェクト？
    # 3. HTMLテンプレートの中で {% url 'account_v1_signup' %} のような形でURLを取得するのに使える
]
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/account/v1/signup/](http://localhost:8000/account/v1/signup/)  

# 次の記事

📖 [Djangoでサインイン（利用開始）のページを作ろう！](https://qiita.com/muzudho1/items/1d34d64562ff07f1742a)  

# 関連する記事

📖 [pennersr / django-allauth](https://github.com/pennersr/django-allauth/blob/master/allauth/templates/account/signup.html) - テンプレートの原型   
📖 [django-allauth Templates](https://django-allauth.readthedocs.io/en/latest/templates.html)  
📖 [Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)  
📖 [【Django】django-allauthのformやhtmlを上書きする方法](https://qiita.com/NOIZE/items/0522825a1de1d6aa4a2b)  

## 認証関連

📖 [【Django】認証のViewをカスタマイズする方法 テンプレート編](https://allneko.club/django/auth-views-customize/)  

## form関連

📖 [Working with forms](https://docs.djangoproject.com/en/4.0/topics/forms/) - 一番詳しい  
📖 [forms.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py) - 原型  
📖 [How can I render Django Form with vuetify?](https://stackoverflow.com/questions/63993890/how-can-i-render-django-form-with-vuetify)  
📖 [vue.js - Vuetifyの入力値でDjangoのテンプレートタグを使用する方法は？](https://tutorialmore.com/questions-2757963.htm)  
📖 [Anyone know how to use vuetify with django form?](https://forum.djangoproject.com/t/anyone-know-how-to-use-vuetify-with-django-form/4807)  
📖 [Source code for django.forms.boundfield](https://docs.djangoproject.com/en/2.2/_modules/django/forms/boundfield/)  
📖 [DjangoのFormクラスを使う](https://qiita.com/taumu/items/4587a91c4d7d2db165b3)  
