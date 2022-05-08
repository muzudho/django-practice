# 目的

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

この記事は Lesson01 から続いていて、順にやってこないと ソースが足りず実行できないので注意されたい。  

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂templates
        │   │   └── 📂members
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📄admin.py
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

# Step 1. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂members
👉                  └── 📄delete.html
```

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

# Step 2. ビュー編集 - v_member.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂members
            │       └── 📄delete.html
            └── 📂views
👉              └── 📄v_member.py
```

```py
from django.http import HttpResponse
from django.template import loader

from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

def deleteMember(request, id=id):
    """メンバー削除"""
    template = loader.get_template('members/delete.html')

    member = Member.objects.get(pk=id)  # idを指定してメンバーを１人取得
    name = member.name  # 名前だけまだ使う
    member.delete()
    context = {
        'member': {
            'name': name
        }
    }
    return HttpResponse(template.render(context, request))
```

# Step 3. urls.pyファイルの編集

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂templates
            │   └── 📂members
            │       └── 📄read.html
            ├── 📂views
            │   └── 📄v_member.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_member
#    ------- -----        --------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # メンバー削除
    path('members/delete/<int:id>/',
         # -----------------------
         # 1
         # 1. `members/delete/<数字列>/` というURLにマッチする。数字列は views.py の中で id という名前で取得できる
         v_member.deleteMember, name='deleteMember'),
    #    ---------------------        ------------
    #    2                            3
    # 2. v_member.py ファイルの deleteMember メソッド
    # 3. HTMLテンプレートの中で {% url 'deleteMember' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

👇 IDの番号は適宜変えてほしい。  

📖 [http://localhost:8000/members/delete/4/](http://localhost:8000/members/delete/4/)  

# 次の記事

📖 [Djangoでモデルのインスタンスの作成／更新ページを作成しよう！](https://qiita.com/muzudho1/items/806ecdba1654ae169f37)  
