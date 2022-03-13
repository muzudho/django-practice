# ログインユーザー一覧

📖 [Djangoで現在ログイン中のユーザ情報を取得したい時](https://awesome-linus.com/2019/04/05/django-get-login-user/)  

# settings.py の設定

INSTALLED_APPS = [
    'webapp1', # 追加
]

# 作成

フォルダーを作成してください。  

📂`host1/webapp1/templates`  

ファイルを作成してください。  

📄`host1/webapp1/templates/login-user-list.html`  


📄host1/webapp1/views.py:  

```py
from django.contrib.auth.decorators import login_required # 追加
from django.template import loader # 追加

# 追加
@login_required
def loginUserList(request):
    # host1/webapp1/templates/webapp1/login-user-list.html を取ってきます
    template = loader.get_template('webapp1/login-user-list.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
```

📖host1/webapp1/urls.py:  

```py
urlpatterns = [
    path('loginUserList', views.loginUserList, name='loginUserList'),
]
```