"""webapp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
import account_pb2_grpc
from webapp1.services import UserService
#    -------
#    1
# 1. アプリケーション フォルダー名

from webapp1.views import v_index
#    ------- -----        -------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

from webapp1.views import v_login_user, v_page1, v_member, v_vuetify_practice, \
    v_read_json_response1, \
    v_read_json_textarea2, v_read_table2o3, v_tic_tac_toe1, v_tic_tac_toe2, \
    v_tic_tac_toe3

urlpatterns = [
    path('', v_index.index, name='index'),
    path('admin/', admin.site.urls),

    # Allauth
    # https://sinyblog.com/django/django-allauth/
    path('', TemplateView.as_view(template_name='home.html'),
         name='home'),  # ログオン後のTOP画面の定義
    path('accounts/', include('allauth.urls')),
    #

    path('practice1/page1', v_page1.page1, name='page1'),
    #     ---------------   -------------        -----
    #     1                 2                    3
    # 1. URLの `practice1/page1` というパスにマッチする
    # 2. v_page1.py ファイルの page1 メソッド
    # 3. HTMLテンプレートの中で {% url 'page1' %} のような形でURLを取得するのに使える

    path('login-user', v_login_user.loginUser, name='loginUser'),
    #     ----------   ----------------------        ---------
    #     1            2                             3
    # 1. URLの `login-user` というパスにマッチする
    # 2. v_login_user.py ファイルの loginUser メソッド
    # 3. HTMLテンプレートの中で {% url 'loginUser' %} のような形でURLを取得するのに使える

    # メンバー一覧
    path('members/', v_member.listMember, name='listMember'),
    #     --------   -------------------        ----------
    #     1          2                          3
    # 1. URLの `members/` というパスにマッチする
    # 2. v_member.py ファイルの listMember メソッド
    # 3. HTMLテンプレートの中で {% url 'listMember' %} のような形でURLを取得するのに使える

    # メンバー読取
    path('members/read/<int:id>/', v_member.readMember, name='readMember'),
    #     ----------------------   -------------------        ----------
    #     1                        2                          3
    # 1. URLの `members/read/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_member.py ファイルの readMember メソッド
    # 3. HTMLテンプレートの中で {% url 'readMember' %} のような形でURLを取得するのに使える

    # メンバー削除
    path('members/delete/<int:id>/',
         # -----------------------
         # 1
         v_member.deleteMember, name='deleteMember'),
    #    ---------------------        ------------
    #    2                            3
    # 1. URLの `members/delete/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_member.py ファイルの deleteMember メソッド
    # 3. HTMLテンプレートの中で {% url 'deleteMember' %} のような形でURLを取得するのに使える

    # メンバー作成
    path('members/create/', v_member.upsertMember, name='createMember'),
    #     ---------------   ---------------------        ------------
    #     1                 2                            3
    # 1. URLの `members/create/` というパスにマッチする
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'createMember' %} のような形でURLを取得するのに使える

    # メンバー更新
    path('members/update/<int:id>/',
         # -----------------------
         # 1
         v_member.upsertMember, name='updateMember'),
    #    ---------------------        ------------
    #    2                            3
    # 1. URLの `members/update/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'updateMember' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify-practice/hello1',
         # ----------------------
         # 1
         v_vuetify_practice.readHello, name='readHello'),
    #     ---------------------------        ---------
    #     2                                  3
    # 1. URLの `vuetify-practice/hello1` というパスにマッチする
    # 2. v_vuetify_practice.py ファイルの readHello メソッド
    # 3. HTMLテンプレートの中で {% url 'readHello' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify-practice/data-table1', v_vuetify_practice.readDataTable1,
         # --------------------------------   ---------------------------------
         # 1                                  2
         name='readDataTable1'),
    #          --------------
    #          3
    # 1. URLの `vuetify-practice/data-table1` というパスにマッチする
    # 2. v_vuetify_practice.py ファイルの readDataTable1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify-practice/data-table2', v_vuetify_practice.readDataTable2,
         # ---------------------------   ---------------------------------
         # 1                             2
         name='readDataTable2'),
    #          --------------
    #          3
    # 1. URLの `vuetify-practice/data-table2` というパスにマッチする
    # 2. v_vuetify_practice.py ファイルの readDataTable2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify-practice/json-textarea1', v_vuetify_practice.readJsonTextarea1,
         # ------------------------------   ------------------------------------
         # 1                                2
         name='readJsonTextarea1'),
    #          -----------------
    #          3
    # 1. URLの `vuetify-practice/json-textarea1` というパスにマッチする
    # 2. v_vuetify_practice.py ファイルの readJsonTextarea1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify-practice/data-table2o2', v_vuetify_practice.readDataTable2o2,
         # -----------------------------   -----------------------------------
         # 1                               2
         name='readDataTable2o2'),
    #          ----------------
    #          3
    # 1. URLの `vuetify-practice/data-table2o2` というパスにマッチする
    # 2. v_vuetify_practice.py ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2o2' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice1/json-response1',
         # -----------------------
         # 1
         # 1. `practice1/json-response1` というURLにマッチする
         v_read_json_response1.readJsonResponse1, name='readJsonResponse1'),
    #                                                   -----------------
    #                                                   2
    # 2. HTMLテンプレートの中で {% url 'readJsonResponse1' %} のような形でURLを取得するのに使える

    path('vuetify2/json-textarea2.html',
         # ---------------------------
         # 1
         # 1. `vuetify2/json-textarea2.html` というURLにマッチする
         v_read_json_textarea2.readJsonTextarea2, name='readJsonTextarea2'),
    #                                                   -----------------
    #                                                   2
    # 2. HTMLテンプレートの中で {% url 'readJsonTextarea2' %} のような形でURLを取得するのに使える

    path('vuetify2/data-table2o3',
         # ---------------------
         # 1
         # 1. `vuetify2/data-table2o3` というURLにマッチする
         v_read_table2o3.readDataTable2o3, name='readDataTable2o3'),
    #                                            ----------------
    #                                            2
    # 2. HTMLテンプレートの中で {% url 'readDataTable2o3' %} のような形でURLを取得するのに使える

    path('tic-tac-toe1/', v_tic_tac_toe1.indexOfTicTacToe1),
    #     -------------
    #     1
    # 1. URLの一部

    path('tic-tac-toe1/<str:room_name>/', v_tic_tac_toe1.playGameOfTicTacToe1),
    #     -----------------------------
    #     1
    # 1. URLの一部。<room_name> に入った文字列は room_name 変数に渡されます

    path('tic-tac-toe2/', v_tic_tac_toe2.indexOfTicTacToe2),
    #                ^                          ^
    #     -------------
    #     1
    # 1. URLの一部

    path('tic-tac-toe2/<str:room_name>/', v_tic_tac_toe2.playGameOfTicTacToe2),
    #                ^                                             ^
    #     -----------------------------
    #     1
    # 1. URLの一部。<room_name> に入った文字列は room_name 変数に渡されます

    path('tic-tac-toe3/', v_tic_tac_toe3.indexOfTicTacToe3),
    #                ^                    ^
    #     -------------
    #     1
    # 1. URLの一部

    path('tic-tac-toe3/<str:room_name>/',
         #           ^
         # ----------------------------
         # 1
         # 1. URLの一部。<room_name> に入った文字列は room_name 変数に渡されます
         v_tic_tac_toe3.playGameOfTicTacToe3),
    #                                          ^
]


def grpc_handlers(server):
    account_pb2_grpc.add_UserControllerServicer_to_server(
        UserService.as_servicer(), server)
