---
title: Djangoでモデルのインスタンスの一覧表示をしよう！
tags: Django Docker
author: muzudho1
slide: false
---
# 目的

Webページ作成を練習したい。以下の簡単な例を説明する。  

`http://localhost:8000/members/` へアクセスすると、  
さきほどモデルを作って管理画面で確認した、データを３件ほど表示したい。  

表示例:  

```plaintext
一覧表示
ID    氏名	       E-Mail                     年齢
----  -----------  -------------------------  ----
1     きふわらね    kifuwarane@example.com	  8
2     きふわらずさ  kifuwarazusa@example.com	  7
3     きふわらかく  kifuwarakaku@example.com	  6
```

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

# Step 1. HTMLファイルの作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/members/list.html`:  

```html
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>メンバー一覧ページ</title>
        <!-- Bootstrap -->
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" />
    </head>
    <body>
        <div class="container">
            <h3>一覧表示</h3>

            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>氏名</th>
                        <th>E-Mail</th>
                        <th>年齢</th>
                    </tr>
                </thead>
                <tbody>
                    {% for member in members %}
                    <tr>
                        <td>{{ member.id }}</td>
                        <td>{{ member.name }}</td>
                        <td>{{ member.email }}</td>
                        <td>{{ member.age }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
</html>
```

# Step 2. views.pyファイルの編集

📄`views.py` は既存だろうから、以下のソースをマージしてほしい。  

📄`host1/webapp1/views.py`:  

```py
from django.http import HttpResponse
from django.shortcuts import render #追加

from .models import Member #追加

# メンバー一覧
def memberList(request):
    template = loader.get_template('members/list.html')
    context = {
        'members':Member.objects.all().order_by('id'), # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))
```

# Step 3. urls.pyファイルの編集

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

📄`host1/webapp1/urls.py`:  

```py
from django.urls import path
from . import views

urlpatterns = [
    # メンバー一覧
    path('members/', views.memberList, name='memberList'), # 追加
]
```

# Step 4. Webの管理画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/members/](http://localhost:8000/members/)  
