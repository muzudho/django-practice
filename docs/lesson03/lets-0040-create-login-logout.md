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
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── <いろいろ>
```

# Step 1. HTMLファイルを置く

以下のディレクトリ、ファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ構造を繰り返す
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

# Step 2. ビュー作成 - v_login_user.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📄login-user.html
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

    @login_required  # 👈 このデコレーターを付けると、ログインしていないなら、認証ページに飛ばします
    @staticmethod
    def render(request):
        """描画"""

        template = loader.get_template('webapp1/login-user.html')
        #                               -----------------------
        #                               1
        # 1. host1/webapp1/templates/webapp1/login-user.html を取得
        #                            -----------------------
        #    webapp1 が２回出てくるのはテクニックのようです

        user = request.user
        context = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return HttpResponse(template.render(context, request))


def render_logout_user(request):
    """ログアウト"""
    logout(request)
    redirect('home')
```

# Step 3. ルート編集 - urls.py ファイル

以下のファイルの該当箇所を追記してほしい

```plaintext
    └── 📂host1
        └── 📂webapp1
            ├── 📂templates
            │   └── 📂webapp1
            │       └── 📄login-user.html
            ├── 📂views
            │   └── 📄v_login_user.py
👉          └── 📄urls.py
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
    path('logout', v_login_user.render_logout_user, name='logoutUser'),
    #     ------   -------------------------------        ----------
    #     1        2                                      3
    # 1. URLの `logout` というパスにマッチする
    # 2. v_login_user.py ファイルの render_logout_user メソッド
    # 3. HTMLテンプレートの中で {% url 'logoutUser' %} のような形でURLを取得するのに使える
]
```

# Step 4. Webページへアクセス

ログインする、ログイン情報を見る:  

📖 [http://localhost:8000/login-user](http://localhost:8000/login-user)  

ログアウトする:  

📖 [http://localhost:8000/logout](http://localhost:8000/logout)  

# 次の記事

📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)  

# 関連する記事

📖 [Using the Django authentication system](https://docs.djangoproject.com/en/3.1/topics/auth/default/)  
