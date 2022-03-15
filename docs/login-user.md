---
title: Djangoでログインユーザー情報を表示しよう！
tags: Django Docker Allauth
author: muzudho1
slide: false
---
# 目的

画面に下記のようなログインしている自分のユーザー情報を表示する方法を説明する。  

```
Login user.
id: 1
username: Muzudho
email: admin@example.com
```

# はじめに

前の記事：　📖 [Djangoでユーザー認証を付けよう！](https://qiita.com/muzudho1/items/55cb7ac55299afd51887)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── （たくさんのもの）
　├── 📂webapp1
　│　　├── 📄settings.py
　│　　├── 📄urls.py
　│　　└── <いろいろ>
　├── 📄.env
　├── 🐳docker-compose.yml
　├── 🐳Dockerfile
　├── 📄manage.py
　└── <いろいろ>
```

# Step 1. HTMLファイルを置く

以下のディレクトリ、ファイルを作成してほしい。  

```plaintext
📂host1
　└── 📂webapp1                      # アプリケーション フォルダー
　 　　└── 📂templates
　 　　　　└── 📂webapp1              # もう１回 アプリケーション フォルダー
　 　　        └── 📄login-user.html
```

📄`host1/webapp1/templates/webapp1/login-user.html`:  

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

# Step 2. views.py を編集

以下のファイルを作成してほしい。  

```plaintext
📂host1
　└── 📂webapp1
　 　　└── 📄views.py
```

📄`host1/webapp1/views.py`:  

```py
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader

@login_required
def loginUser(request):
    template = loader.get_template('webapp1/login-user.html')

    user = request.user
    context = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return HttpResponse(template.render(context, request))
```

# Step 3. urls.py を編集

以下のファイルの該当箇所を追記してほしい

📄`host1/webapp1/urls.py`:  

```py
urlpatterns = [
    path('login-user', views.loginUser, name='loginUser'), # 追加
]
```

# Step 4. Webページへアクセス

📖 [http://localhost:8000/login-user](http://localhost:8000/login-user)  

# 次の記事

📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)  
