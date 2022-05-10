# 目的

（※いわゆる CRUD の C と U）  

`http://localhost:8000/members/upsert/4/` へアクセスすると、  
id が 4 のメンバーが存在しないときは新規作成を、  
id が 4 のメンバーが既に存在するなら更新をしたい。  

👇 表示例（新規作成のとき）:  

```plaintext
会員の作成

氏名:                       E-Mail:                     年齢:
      --------------------         --------------------      --------------------

送信
戻る
```

👇 表示例（更新のとき）:  

```plaintext
会員の更新

氏名: ほげ                  E-Mail: hoge@example.com     年齢: 3
      --------------------         --------------------       --------------------

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
👉                  └── 📄upsert.html
```

```html
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>会員の作成/更新</title>
        <!-- Bootstrap -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous" />
    </head>
    <body>
        <div class="container">

            {% if id %}
            <h3 class="page-header">会員の更新</h3>
            <form action="{% url 'updateMember' id=id %}" method="post" class="form-horizontal" role="form">
            {% else %}
            <h3 class="page-header">会員の作成</h3>
            <form action="{% url 'createMember' %}" method="post" class="form-horizontal" role="form">
            {% endif %}

                {% csrf_token %}
                {{ form }}

                <div class="form-group">
                    <div class="col-sm-offset-2 col-sm-10">
                        <button type="submit" class="btn btn-primary">送信</button>
                    </div>
                </div>

            </form>
            <a href="{% url 'listMember' %}" class="btn btn-default btn-sm">戻る</a>
        </div>
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
</html>
```

# Step 2. フォーム作成 - f_member.py ファイル

HTMLタグの `<form>～</form>` の子要素を自動生成させよう。  

以下のファイルを作成してほしい。  

📄`host1/webapp1/forms/f_member.py`:  
```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂forms
👉          │   └── 📄f_member.py
            └── 📂templates
                └── 📂members
                    └── 📄upsert.html
```

```py
from django.forms import ModelForm

from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MemberForm(ModelForm):
    class Meta:
        model = Member  # モデル指定
        fields = ('name', 'email', 'age',)  # フィールド指定
```

# Step 3. ビュー編集 - v_member.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂forms
            │   └── 📄f_member.py
            ├── 📂templates
            │   └── 📂members
            │       └── 📄upsert.html
            └── 📂views
👉              └── 📄v_member.py
```

```py
from django.shortcuts import render, get_object_or_404, redirect

from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.forms.f_member import MemberForm
#    ------- ----- --------        ----------
#    1       2     3               4
# 1. アプリケーション フォルダー名
# 2. Python ファイル名。拡張子抜き
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

def upsertMember(request, id=None):
    """メンバーの作成または更新"""

    if id:  # idがあるとき（更新の時）
        # idで検索して、結果を戻すか、404エラー
        member = get_object_or_404(Member, pk=id)
    else:  # idが無いとき（作成の時）
        member = Member()

    # POSTの時（作成であれ更新であれ送信ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():  # バリデーションがOKなら保存
            member = form.save(commit=False)
            member.save()
            return redirect('listMember')
    else:  # GETの時（フォームを生成）
        form = MemberForm(instance=member)

    # 作成・更新画面を表示
    return render(request, 'members/upsert.html', dict(form=form, id=id))
```

# Step 4. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂forms
            │   └── 📄f_member.py
            ├── 📂templates
            │   └── 📂members
            │       └── 📄upsert.html
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

    # メンバー作成
    path('members/create/', v_member.upsertMember, name='createMember'),
    #     ---------------   ---------------------        ------------
    #     1                 2                            3
    # 1. `members/create/` というURLにマッチする
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'createMember' %} のような形でURLを取得するのに使える

    # メンバー更新
    path('members/update/<int:id>/',
         # -----------------------
         # 1
         # 1. `members/update/<数字列>/` というURLにマッチする。数字列は views.py の中で id という名前で取得できる
         v_member.upsertMember, name='updateMember'),
    #    ---------------------        ------------
    #    2                            3
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'updateMember' %} のような形でURLを取得するのに使える
]
```

# Step 5. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

👇 作成するとき、IDは付けるな。  

📖 [http://localhost:8000/members/create/](http://localhost:8000/members/create/)  

👇 更新するとき、IDを付けろ。 IDは適宜変えてほしい。  

📖 [http://localhost:8000/members/update/5/](http://localhost:8000/members/update/5/)  

# 次の記事

📖 [DjangoでフロントエンドにVuetifyを使おう！](https://qiita.com/muzudho1/items/e80a72b027249daa4d41)

# 参考にした記事

📖 [DjangoでCRUD](https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92)
