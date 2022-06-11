# 目的

（※いわゆる CRUD の C と U）  

`http://localhost:8000/rooms/upsert/4/` へアクセスすると、  
id が 4 の部屋が存在しないときは新規作成を、  
id が 4 の部屋が既に存在するなら更新をしたい  

👇 表示例（新規作成のとき）:  

```plaintext
部屋の作成

部屋名:                       盤面:                     棋譜:
       --------------------       --------------------     --------------------

送信
戻る
```

👇 表示例（更新のとき）:  

```plaintext
部屋の更新

部屋名: Lion                  盤面: XOXOXOXOX            年齢: 012345678
       --------------------       --------------------      --------------------

送信
戻る
```

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

参考にした元記事は 📖[DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

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
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   ├── 📂webapp1
        │   │   │   ├── 📂practice
        │   │   │   │   └── 📄vuetify-desserts.json
        │   │   │   └── 📂tic-tac-toe
        │   │   │       ├── 📂v1
        │   │   │       │   └── 📄<いろいろ>
        │   │   │       └── 📂v2
        │   │   │           └── 📄<いろいろ>.js
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂rooms
        │   │       │   └── 📄<いろいろ>.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂tic_tac_toe1
        │   │   └── 📄consumer1.py
        │   ├── 📂tic-tac-toe2
        │   │   ├── consumer1.py
        │   │   └── message_converter.py
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂websock_practice1
        │   │       └── 📂v1
        │   │           └── 📄<いろいろ>.py
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

# Step 1. HTMLファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂rooms
👉                      └── 📄upsert.html
```

```html
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>部屋の作成/更新</title>
        <!-- Bootstrap -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />
    </head>
    <body>
        <div class="container">

            {% if id %}
            <h3 class="page-header">部屋の更新</h3>
            <form action="{% url 'updateRoom' id=id %}" method="post" class="form-horizontal" role="form">
            {% else %}
            <h3 class="page-header">部屋の作成</h3>
            <form action="{% url 'createRoom' %}" method="post" class="form-horizontal" role="form">
            {% endif %}

                {% csrf_token %}
                {{ form }}

                <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-10">
                        <button type="submit" class="btn btn-primary">送信</button>
                    </div>
                </div>

            </form>
            <a href="{% url 'listRoom' %}" class="btn btn-default btn-sm">戻る</a>
        </div>
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
</html>
```

# Step 2. フォーム作成 - f_room.py ファイル

HTMLタグの `<form>～</form>` の子要素を自動生成させよう。  

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂forms
👉          │   └── 📄f_room.py
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂rooms
                        └── 📄upsert.html
```

```py
from django.forms import ModelForm

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class RoomForm(ModelForm):
    class Meta:
        model = Room  # モデル指定
        fields = ('name', 'board', 'record',)  # フィールド指定
```

# Step 3. ビュー編集 - v_room.py ファイル

📄`v_room.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂forms
            │   └── 📄f_room.py
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂rooms
            │           └── 📄upsert.html
            └── 📂views
👉              └── 📄v_room.py
```

```py
from django.shortcuts import render, get_object_or_404, redirect

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.forms.f_room import RoomForm
#    ------- ----- ------        --------
#    1       2     3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class RoomView():
    """部屋"""

    # ...中略...

    @staticmethod
    def render_upsert(request, id=None):
        """作成または更新のページ"""

        if id:  # idがあるとき（更新の時）
            # idで検索して、結果を戻すか、404エラー
            room = get_object_or_404(Room, pk=id)
        else:  # idが無いとき（作成の時）
            room = Room()

        # POSTの時（作成であれ更新であれ送信ボタンが押されたとき）
        if request.method == 'POST':
            # フォームを生成
            form = RoomForm(request.POST, instance=room)
            if form.is_valid():  # バリデーションがOKなら保存
                room = form.save(commit=False)
                room.save()
                return redirect('listRoom')
        else:  # GETの時（フォームを生成）
            form = RoomForm(instance=room)

        # 作成・更新画面を表示
        return render(request, 'webapp1/rooms/upsert.html', dict(form=form, id=id))
        #                       -------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/rooms/upsert.html
        #                            -------------------------
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂forms
            │   └── 📄f_room.py
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂rooms
            │           └── 📄upsert.html
            ├── 📂views
            │   └── 📄v_room.py
👉          └── 📄urls.py
```

```py
from django.urls import path

from webapp1.views import v_room
#    ------- -----        ------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...中略...

    # +----
    # | 部屋

    # 作成
    path('rooms/create/', v_room.RoomView.render_upsert, name='createRoom'),
    #     -------------   -----------------------------        ----------
    #     1               2                                    3
    # 1. 例えば `http://example.com/rooms/create/` のような URL のパスの部分
    #                              --------------
    # 2. v_room.py ファイルの RoomView クラスの render_upsert 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'createRoom' %} のような形でURLを取得するのに使える

    # 更新
    path('rooms/update/<int:id>/',
         # ---------------------
         # 1
         v_room.RoomView.render_upsert, name='updateRoom'),
    #    -----------------------------        ----------
    #    2                                    3
    # 1. 例えば `http://example.com/rooms/update/<数字列>/` のような URL のパスの部分。数字列は v_room.py の中で id という名前で取得できる
    #                              ----------------------
    # 2. v_room.py ファイルの RoomView クラスの render_upsert 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'updateRoom' %} のような形でURLを取得するのに使える

    # | 部屋
    # +----
]
```

# Step 5. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

👇 作成するとき、IDは付けるな。  

📖 [http://localhost:8000/rooms/create/](http://localhost:8000/rooms/create/)  

👇 更新するとき、IDを付けろ。 IDは適宜変えてほしい。  

📖 [http://localhost:8000/rooms/update/5/](http://localhost:8000/rooms/update/5/)  

# 次の記事

📖 [Djangoでゲームポータルページを作ろう！](https://qiita.com/muzudho1/items/0c59f3ce7aa6bef2a91f)  

# 参考にした記事

📖 [DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92)
