# ログインユーザー情報取得

📖 [Djangoで現在ログイン中のユーザ情報を取得したい時](https://awesome-linus.com/2019/04/05/django-get-login-user/)  

# settings.py の設定

INSTALLED_APPS = [
    'webapp1', # 追加
]

# 作成

フォルダーを作成してください。  

📂`host1/webapp1/templates`  

ファイルを作成してください。  

📄`host1/webapp1/templates/webapp1/login-user.html`  

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

📄host1/webapp1/views.py:  

```py
from django.contrib.auth.decorators import login_required # 追加
from django.template import loader # 追加

# 追加
@login_required
def loginUser(request):
    # host1/webapp1/templates/webapp1/login-user.html を取ってきます。 webapp1 が２回出てくるのはテクニックのようです
    template = loader.get_template('webapp1/login-user.html')

    user = request.user
    context = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return HttpResponse(template.render(context, request))
```

📖host1/webapp1/urls.py:  

```py
urlpatterns = [
    path('login-user', views.loginUser, name='loginUser'), # 追加
]
```

# Webページへアクセス

📖 [http://localhost:8000/login-user](http://localhost:8000/login-user)  

# Documents

📖 [Djangoでログインユーザー情報を表示しよう！](https://qiita.com/muzudho1/items/9f1ae4d0debc0b8aa4b1)  
