# 目的

Django に最初から付いている User モデルを拡張したい  

試しに 対局マッチング状況を表す match_state プロパティを追加するものとし、  
その値は 整数とし、  
0 を休憩中， 1 を対局申込中， 2 を対局案内中， 3 を対局中， 4 を観戦中 とする  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

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
        │   ├── 📂models_helper
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   ├── 📂webapp1
        │   │   │   └── 📂tic-tac-toe
        │   │   │       ├── 📂v1
        │   │   │       └── 📂v2
        │   │   │           └── 📄<いろいろ>.js
        │   │   ├── 📂<いろいろ>-practice
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂tic-tac-toe
        │   │       │   ├── 📂v1
        │   │       │   └── 📂v2
        │   │       │       └── 📄<いろいろ>.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📂practice
        │   │       └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄routing1.py
        │   └── 📄urls.py
        ├── 📄.env
        ├── 📄asgi.py
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        └── 📄urls.py
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. テンプレート編集 - user-list-v2.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
👉                      └── 📄user-list-v2.html
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<!-- See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92 -->
<html lang="ja">
    <head>
        <meta charset="utf-8" />
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>会員登録ユーザー一覧</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <!-- v-app-bar に app プロパティを指定しないなら、背景画像を付けてほしい -->
                <v-app-bar app dense elevation="4">
                    <v-app-bar-nav-icon></v-app-bar-nav-icon>
                    <v-toolbar-title>ゲーム対局サーバー</v-toolbar-title>
                </v-app-bar>
                <v-main>
                    <v-container>
                        <h3>会員登録ユーザー一覧</h3>
                        <v-simple-table>
                            <template v-slot:default>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>ユーザー名</th>
                                        <th>アクティブか</th>
                                        <th>最終ログイン</th>
                                        <th>マッチング状態</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="user in vu_userDic" :key="user.pk">
                                        {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %} {% verbatim %}
                                        <td>{{ user.pk }}</td>
                                        <td>{{ user.username }}</td>
                                        <td>{{ user.is_active }}</td>
                                        <td>{{ user.last_login }}</td>
                                        <td>{{ user.match_state }}</td>
                                        {% endverbatim %}
                                    </tr>
                                </tbody>
                            </template>
                        </v-simple-table>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // "vu_" は 「vue1.dataのメンバー」 の目印
                    vu_userDic: JSON.parse("{{ dj_user_dic|escapejs }}"),
                },
            });
        </script>
    </body>
</html>
```

# Step 3. User モデル拡張 - m_user_profile.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models
👉          │   └── 📄m_user_profile.py
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂practice
                        └── 📄user-list-v2.html
```

```py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    # この User オブジェクトの下に Profile オブジェクトをぶら下げると思ってください
    #
    # Example
    # -------
    #
    # user = User.objects.get(pk=user_id)
    # print(user.profile.match_state)
    #
    # OneToOneField - 1対1対応のリレーション。 デフォルトで Unique 属性
    #
    # * `on_delete` - 必須。 models.CASCADE なら、親テーブルのレコードが消されると、子テーブルのレコードも削除されます
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)

    # 対局のマッチング状態
    #
    # 0 を休憩中， 1 を対局申込中， 2 を対局案内中， 3 を対局中， 4 を観戦中 とする
    #
    # * `blank` - 未指定でもセーブを受け入れるなら真
    # * `default` - 初期値
    match_state = models.IntegerField(
        '対局のマッチング状態', null=True, blank=True, default=0)

    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return f"{self.user}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """新規作成"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存"""
    instance.profile.save()


# この行が要るのか分からない（＾～＾）
# 📖 [Extending the User model with custom fields in Django](https://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django)
# post_save.connect(create_user_profile, sender=User)
```

# Step 4. モデル作成 - コマンド実行

```shell
# cd host1

docker-compose run --rm web python3 manage.py makemigrations webapp1
#                                                            -------
#                                                            1
# 1. アプリケーション ディレクトリー名
```

以下のディレクトリーとファイルが生成される。  

```plaintext
    └── 📂host1
        └── 📂webapp1
            └── 📂migrations
                ├── 📄__init__.py
                └── 📄0001_initial.py   # ファイル名はこの通りとは限らない
```

👆 これらのファイルは マイグレーション ファイル と呼ぶらしい。  

# Step 5. コマンド実行＜その２＞

```shell
docker-compose run --rm web python3 manage.py showmigrations
```

👆 マイグレーションする前に、マイグレーションの対象になっているものを確認  

```shell
docker-compose run --rm web python3 manage.py migrate
```

👆 ここまでやって マイグレーション という作業が終わるらしい。  

```shell
docker-compose run --rm web python3 manage.py showmigrations
```

👆 マイグレーションした後に、マイグレーションされたものを確認  

# Step 6. 管理画面へ登録 - admin.py ファイル編集

以下のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models
            │   └── 📄m_user_profile.py
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄user-list-v2.html
👉          └── 📄admin.py
```

```py
from .models.m_user_profile import Profile

# ... 中略 ...

admin.site.register(Profile)
```

👆 管理画面に Profile オブジェクトが表示されるようにした  

# Step 7. スーパーユーザーでWebの管理画面へアクセス

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

👆 Profile モデルに、 User データに紐づくデータを登録しておいてほしい  

# Step 8. モデルヘルパー作成 - mh_user.py ファイル

既存の以下のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models
            │   └── 📄m_user_profile.py
            ├── 📂models_helper
👉          │   └── 📄mh_user.py
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄user-list-v2.html
            └── 📄admin.py
```

```py
import json
from django.contrib.auth import get_user_model
from django.core import serializers

from webapp1.models.m_user_profile import Profile
#    ------- ------ --------------        -------
#    1       2      3                     4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MhUser():

    @staticmethod
    def get_user_dic_v2():
        """会員登録ユーザー一覧 v2"""
        User = get_user_model()

        # 会員登録ユーザー一覧
        # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
        user_table_qs = User.objects.all().select_related('profile')  # QuerySet
        #                                 --------------------------
        #                                 1
        # 1. これを付けて何が起こっているか分からないが、サンプルでよく付けているのを見かけるので真似する。外しても動く。
        #    User クラスを拡張して作った Profile クラスの OneToOneField フィールドの名前を指しています
        # print(f"user_table_qs={user_table_qs}")
        #
        user_table_json = serializers.serialize('json', user_table_qs)
        user_table_doc = json.loads(user_table_json)
        # print(f"user_table_doc={json.dumps(user_table_doc, indent=4)}")

        # 使いやすい形に変換します
        user_dic = dict()
        for user_rec in user_table_doc:  # User Record
            # print(f"user_rec={user_rec}")
            username = user_rec["fields"]["username"]
            # print(f"user_rec['fields']['username']={username}")

            # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
            profile_table_qs = Profile.objects.filter(  # QuerySet
                #                             -------
                #                             1
                user__username=username) # TODO ★ ここは pk じゃなくて大丈夫か？
            # 1. filter ならインスタンスが返ってくる。 get なら文字列表現が返ってくる
            # QuerySet は中身が見えないので JSON にダンプするのが定番
            # print(f"Profile={profile_table_qs}")
            #
            profile_table_json = serializers.serialize(
                'json', profile_table_qs)
            profile_table_doc = json.loads(profile_table_json)  # オブジェクト
            # print(f"profile_table_doc={json.dumps(profile_table_doc, indent=4)}")

            user_dic[user_rec["pk"]] = {
                "pk": user_rec["pk"],
                "last_login": user_rec["fields"]["last_login"],
                "username": user_rec["fields"]["username"],
                "is_active": user_rec["fields"]["is_active"],

                "match_state": profile_table_doc[0]["fields"]["match_state"],
                #                               ---
                #                               1
                # 1. 先頭の1件を取っている
            }

        return user_dic
```

# Step 9. ビュー編集 - pages.py ファイル

以下の既存ファイルに、ソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂models
            │   └── 📄m_user_profile.py
            ├── 📂models_helper
            │   └── 📄mh_user.py
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂practice
            │           └── 📄user-list-v2.html
            ├── 📂views
            │   └── 📂practice
👉          │       └── 📄pages.py
            └── 📄admin.py
```

```py
import json
from django.shortcuts import render

from webapp1.models_helper.mh_user import MhUser
#    ------- ------------- -------        ------
#    1       2             3              4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def render_user_list_v2(request):
    """会員登録ユーザー一覧 v2"""

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # Vue に渡すときは、 JSON オブジェクトではなく、 JSON 文字列です
        'dj_user_dic': json.dumps(MhUser.get_user_dic_v2()),
        #                                            ---
    }

    return render(request, "webapp1/practice/user-list-v2.html", context)
    #                       ----------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/practice/user-list-v2.html
    #                            ----------------------------------
```

# Step 10. ルート編集 - urls.py ファイル

以下の既存のファイルに、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models_helper
        │   │   └── 📄mh_user.py
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂practice
        │   │           └── 📄user-list-v2.html
        │   ├── 📂views
        │   │   └── 📂practice
        │   │       └── 📄pages.py
👉      │   └── 📄urls.py                       # こちら
❌      └── 📄urls.py                           # これではない
```

```py
from webapp1.views.practice import pages as practice_pages
#    ------- --------------        -----    --------------
#    1       2                     3        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [
    # ...中略...

    # 会員登録ユーザー一覧 v2
    path('practice/user-list/v2/',
         # ---------------------
         # 1
         practice_pages.render_user_list_v2, name='practice_userListV2'),
    #    ----------------------------------        -------------------
    #    2                                         3
    #
    # 1. 例えば `http://example.com/practice/user-list/v2/` のような URL のパスの部分
    #                              -----------------------
    # 2. practice_pages (別名)ファイルの render_user_list_v2 メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_userListV2' %} のような形でURLを取得するのに使える
]
```

# Step 11. Web画面へアクセス

📖 [http://localhost:8000/practice/user-list/v2/](http://localhost:8000/practice/user-list/v2/)  

# 次の記事

📖 [Djangoで自動リロードするページを作ろう！](https://qiita.com/muzudho1/items/8df599dc0e0acb25f649)  

# 参考にした記事

📖 [How to Extend Django User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html)  
📖 [【django】モデルのフィールドについて：フィールドの型・オプション一覧](https://office54.net/python/django/model-field-options)  
📖 [DjangoでMigrationsのリセット方法（既存のデータベースを残したまま）](https://dot-blog.jp/news/how-to-reset-django-migrations/)  
📖 [Django : How to use select_related for a OneToOneField?](https://stackoverflow.com/questions/38701919/django-how-to-use-select-related-for-a-onetoonefield)  
📖 [Django2.0から必須になったon_deleteの使い方](https://djangobrothers.com/blogs/on_delete/)  
📖 [【django】モデルのリレーションフィールド：ForeignKey、OneToOneField、ManyToManyField](https://office54.net/python/django/model-field-relation)  
📖 [One-to-one relationships](https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/)  
📖 [One-To-One Relationship (OneToOneField)](https://medium.com/django-rest/one-to-one-relationships-onetoonefield-917cfd2e4ce3)  
📖 [Managers](https://docs.djangoproject.com/en/4.0/topics/db/managers/)  
📖 [Django 'model' object is not iterable](https://stackoverflow.com/questions/56374741/django-model-object-is-not-iterable)  
