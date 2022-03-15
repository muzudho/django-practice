---
title: Djangoでモデルのインスタンスの削除ページを作成しよう！
tags: Django Docker crud
author: muzudho1
slide: false
---
# 目的

Webページ作成を練習したい。以下の簡単な例を説明する。  
（※いわゆる CRUD の D）  

`http://localhost:8000/members/delete/4/` へアクセスすると、  
id が 4 のメンバーを削除したい。  

表示例:  

```plaintext
会員の削除

「ほげ」を削除しました。

戻る
```

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                         | Value                                                                                                      |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1. モデルを作っておくこと   | 📖[Djangoでモデルを追加しよう！](https://qiita.com/muzudho1/items/2463cc006da69f5ed7b2)                     |
| 2. 一覧表示を作っておくこと | 📖[Djangoでモデルのインスタンスの一覧表示をしよう！](https://qiita.com/muzudho1/items/77668130b6d941596327) |

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
　│　　│    ├── 📂members
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

📄`host1/webapp1/templates/members/delete.html`:  

```html
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>メンバー削除</title>
        <!-- Bootstrap -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />
    </head>
    <body>
        <div class="container">
            <h3>会員の削除</h3>
            <div class="card" style="width: 18rem">「{{ member.name }}」を削除しました。</div>
            <a href="{% url 'listMember' %}" class="btn btn-default btn-sm">戻る</a>
        </div>
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
</html>
```

# Step 2. views.pyファイルの編集

📄`views.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/views.py`:  

```py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404 #追加

from .models import Member #追加

# メンバー削除
def deleteMember(request, id=id):
    template = loader.get_template('members/delete.html')

    member = Member.objects.get(pk=id) # idを指定してメンバーを１人取得
    name = member.name # 名前だけ取得しておく
    member.delete()
    context = {
        'member': {
            'name' : name
        }
    }
    return HttpResponse(template.render(context, request))
```

# Step 3. urls.pyファイルの編集

📄`urls.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/urls.py`:  

```py
from django.urls import path
from . import views

urlpatterns = [
    # メンバー一覧
    path('members/', views.listMember, name='listMember'), # 追加
    #                                        ----------
    #                                        1
    # 1. HTMLテンプレートの中で {% url 'listMember' %} のような形でURLを取得するのに使える

    # メンバー削除
    path('members/delete/<int:id>/', views.deleteMember, name='deleteMember'), # 追加
    #     ------------------------
    #     1
    # 1. `members/delete/<数字列>/` というURLにマッチする。数字列は views.py の中で id という名前で取得できる
]
```

# Step 4. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

👇 IDの番号は適宜変えてほしい。  

📖 [http://localhost:8000/members/delete/4/](http://localhost:8000/members/delete/4/)  

