# 目的

さきほどモデルを作り、データを保存した。そこで、サーバーに保存したデータを表示したい。  
いわゆる CRUD（クラッド）の R。  

# はじめに

前提知識:  

| Key                    | Value                                                                                 |
| ---------------------- | ------------------------------------------------------------------------------------- |
| モデルを作っておくこと | [Djangoでモデルを追加しよう！](https://qiita.com/muzudho1/items/2463cc006da69f5ed7b2) |

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

参考にした元記事は 📖[DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📂templates
　│　　│    └── 📂webapp1
　│　　│        └── 📄<いろいろ>.html
　│　　├── 📄admin.py
　│　　├── 📄models.py
　│　　├── 📄settings.py
　│　　├── 📄urls.py
　│　　├── 📄views.py
　│　　└── <いろいろ>
　├── 📄.env
　├── 🐳docker-compose.yml
　├── 🐳Dockerfile
　├── 📄manage.py
　└── <いろいろ>
```

# HTMLファイルの作成＜その１＞

（なんだかよく分からないが）以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/members/base1.html`:  

```html
{% load staticfiles %}
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}My books{% endblock %}</title>
    <!-- Bootstrap -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
    <div class="container">
      {% block content %}
        {{ content }}
      {% endblock %}
    </div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <!-- jsを書く場所 -->
    {% block script %}
    {% endblock %}
  </body>
</html>
```

👆 Webページ１個分のHTMLファイルになっている。ただし、あとで 穴埋め する穴の空いた形をしている。  

# HTMLファイルの作成＜その２＞

（なんだかよく分からないが）以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/members/read.html`:  

```html
{% extends "base1.html" %}
{% load bootstrap %}

{% block title %}会員の詳細{% endblock title %}

{% block content %}
    <h3>会員の詳細情報</h3>
    <h5>名前</h5>
    {{ member.name }}
    <h5>E-Mail</h5>
    {{ member.email }}
    <h5>年齢</h5>
    {{ member.age }}
    <br>
    <br>
    <a href="{% url 'crud:index' %}" class="btn btn-default btn-sm">戻る</a>
{% endblock content %}
```

👆 穴が開いていた 📄`base1.html` の `block` の箇所の穴を埋めるものだ。  

# views.pyファイルの編集

📄`views.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/views.py`:  

```py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404 #追加

from .models import Member #追加

# メンバー読取ページ
def memberRead(request, id=id):
    member = get_object_or_404(Member, pk=id)
    return render(request, 'members/read.html', {'member':member})
```

# urls.pyファイルの編集

📄`urls.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/urls.py`:  

```py
from django.urls import path
from . import views

urlpatterns = [
    # メンバー
    path('members/read', views.memberRead, name='memberRead'), # 追加
]
```

# Webの管理画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/members/read](http://localhost:8000/members/read)  
