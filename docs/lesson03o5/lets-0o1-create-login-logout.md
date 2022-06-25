# 目的

ログインしている自分のユーザー情報を表示したい。  
フォーマットは以下のように考えている  

```
Login user.

* id: 1
* username: Muzudho
* email: admin@example.com
```

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ構造を繰り返す
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📄urls.py
        │   └── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        └── 📄urls.py
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 設定編集 - settings.py ファイル

以下のように該当箇所を追加してほしい。  

```plaintext
    └── 📂host1
👉      └── 📄settings.py
```

👇 レッスンの進み具合によって、 URL などを変えてください  

```py
# ログインしていないときに飛ばされる先。指定しないと '/accounts/login/'
LOGIN_URL = '/accounts/v1/login/'  # 慣れない内は URL で指定
# LOGIN_URL = 'login' # 慣れてくれば name で指定
```

# Step 3. HTMLファイルを置く

以下のディレクトリ、ファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ構造を繰り返す
                    └── 📂practice
                        └── 📄login-user.html
```

```html
<html>
    <body>
        Login user.
        <ul>
            <li>id: {{ id }}</li>
            <li>username: {{ username }}</li>
            <li>email: {{ email }}</li>
        </ul>
    </body>
</html>
```

# Step 4. ビュー作成 - v_login_user.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📂practice
            │           └── 📄login-user.html
            └── 📂views
👉              └── 📄v_login_user.py
```

```py
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import redirect


class LoggingIn():
    """ログイン中"""

    _path_of_html = "webapp1/practice/login-user.html"
    #                --------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/practice/login-user.html を取得
    #                            --------------------------------

    # 👇 このデコレーターを付けると、ログインしていないなら、 settings.py の LOGIN_URL で指定した URL に飛ばします。
    # インスタンスのメソッドや、クラスメソッドには付けられません。
    # 第一引数が self や clazz でないことに注意してください
    @login_required
    def render(request):
        """描画"""
        return loggingIn_render(request, LoggingIn._path_of_html)


class LoggingOut():
    """ログアウト中"""

    def render(request):
        """描画"""
        return loggingOut_render(request)


# 以下、関数


def loggingIn_render(request, path_of_html):
    """ログイン中 - 描画"""
    template = loader.get_template(path_of_html)

    user = request.user
    context = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return HttpResponse(template.render(context, request))


def loggingOut_render(request):
    """ログアウト中 - 描画"""
    logout(request)  # Django の認証機能のログアウトを使う
    return redirect('home')  # ホームに戻る
```

# Step 5. ルート編集 - urls.py ファイル

以下のファイルの該当箇所を追記してほしい

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂templates
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄login-user.html
        │   ├── 📂views
        │   │   └── 📄v_login_user.py
👉      │   └── 📄urls.py                       # こちら
❌      └── 📄urls.py                           # これではない
```

```py
# 冒頭
from webapp1.views import v_login_user
#    ------- -----        ------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

# ...中略...

urlpatterns = [
    # ...中略...

    # ログイン
    path('login-user', v_login_user.LoggingIn.render, name='loginUser'),
    #     ----------   -----------------------------        ---------
    #     1            2                                    3
    # 1. 例えば `http://example.com/login-user` のような URL のパスの部分
    #                              -----------
    # 2. v_login_user.py ファイルの LoggingIn クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('logout', v_login_user.LoggingOut.render, name='logoutUser'),
    #     ------   ------------------------------        ----------
    #     1        2                                     3
    # 1. 例えば `http://example.com/logout` のような URL のパスの部分
    #                              -------
    # 2. v_login_user.py ファイルの LoggingOut クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'logoutUser' %} のような形でURLを取得するのに使える
]
```

# Step 6. Webページへアクセス

ログインする、ログイン情報を見る:  

📖 [http://localhost:8000/login-user](http://localhost:8000/login-user)  

ログアウトする:  

📖 [http://localhost:8000/logout](http://localhost:8000/logout)  

# 次の記事

📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)  

# 関連する記事

📖 [Using the Django authentication system](https://docs.djangoproject.com/en/3.1/topics/auth/default/)  
📖 [Djangoメモ(25) : login_requiredデコレータでビューをログイン済みユーザーのみに制限](https://wonderwall.hatenablog.com/entry/2018/03/25/180000)  
