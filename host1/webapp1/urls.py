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
    v_json_practice, v_tic_tac_toe_v1, v_tic_tac_toe_v2, v_tic_tac_toe_v2o1, v_tic_tac_toe3, \
    v_room, v_home_v2, v_lobby_v1

urlpatterns = [
    path('', v_index.index, name='index'),


    # +----
    # | Allauth

    # 管理画面に入りたい
    path('admin/', admin.site.urls),
    #     ------   ---------------
    #     1        2
    # 1. URLの `admin/` というパスにマッチする
    # 2. 最初から用意されている URL？

    # https://sinyblog.com/django/django-allauth/
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #    --  -----------------------------------------------        ----
    #    1   2                                                      3
    # 1. URL に パスを付けなかったときにマッチする
    # 2. 最初から用意されているページ？
    # 3. ログイン後に飛んでくるページの URL のパスを 'home' という名前で覚えておく

    path('accounts/', include('allauth.urls')),
    #     ---------   -----------------------
    #     1           2
    # 1. URLの `accounts/` というパスにマッチする
    # 2. 最初から用意されているURL？

    # | Allauth
    # +----




    # +----
    # | 練習１
    path('practice1/page1', v_page1.page1, name='page1'),
    #     ---------------   -------------        -----
    #     1                 2                    3
    # 1. URLの `practice1/page1` というパスにマッチする
    # 2. v_page1.py ファイルの page1 メソッド
    # 3. HTMLテンプレートの中で {% url 'page1' %} のような形でURLを取得するのに使える
    # | 練習１
    # +----




    # +----
    # | ログイン

    # ログイン
    path('login-user', v_login_user.loginUser, name='loginUser'),
    #     ----------   ----------------------        ---------
    #     1            2                             3
    # 1. URLの `login-user` というパスにマッチする
    # 2. v_login_user.py ファイルの loginUser メソッド
    # 3. HTMLテンプレートの中で {% url 'loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('logout', v_login_user.logoutUser, name='logoutUser'),
    #     ------   -----------------------        ----------
    #     1        2                              3
    # 1. URLの `logout` というパスにマッチする
    # 2. v_login_user.py ファイルの logoutUser メソッド
    # 3. HTMLテンプレートの中で {% url 'logoutUser' %} のような形でURLを取得するのに使える

    # | ログイン
    # +----




    # +----
    # | 会員

    # 会員一覧
    path('members/', v_member.listMember, name='listMember'),
    #     --------   -------------------        ----------
    #     1          2                          3
    # 1. URLの `members/` というパスにマッチする
    # 2. v_member.py ファイルの listMember メソッド
    # 3. HTMLテンプレートの中で {% url 'listMember' %} のような形でURLを取得するのに使える

    # 会員読取
    path('members/read/<int:id>/', v_member.readMember, name='readMember'),
    #     ----------------------   -------------------        ----------
    #     1                        2                          3
    # 1. URLの `members/read/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_member.py ファイルの readMember メソッド
    # 3. HTMLテンプレートの中で {% url 'readMember' %} のような形でURLを取得するのに使える

    # 会員削除
    path('members/delete/<int:id>/',
         # ------------------------
         # 1
         v_member.deleteMember, name='deleteMember'),
    #   ---------------------        ------------
    #   2                            3
    # 1. URLの `members/delete/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_member.py ファイルの deleteMember メソッド
    # 3. HTMLテンプレートの中で {% url 'deleteMember' %} のような形でURLを取得するのに使える

    # 会員作成
    path('members/create/', v_member.upsertMember, name='createMember'),
    #     ---------------   ---------------------        ------------
    #     1                 2                            3
    # 1. URLの `members/create/` というパスにマッチする
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'createMember' %} のような形でURLを取得するのに使える

    # 会員更新
    path('members/update/<int:id>/',
         # -----------------------
         # 1
         v_member.upsertMember, name='updateMember'),
    #    ---------------------        ------------
    #    2                            3
    # 1. URLの `members/update/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'updateMember' %} のような形でURLを取得するのに使える

    # | 会員
    # +----



    # +----
    # | Vuetify練習

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
    path('json-practice/response1',
         # ----------------------
         # 1
         v_json_practice.readJsonResponse1, name='readJsonResponse1'),
    #    ---------------------------------        -----------------
    #    2                                        3
    # 1. URLの `practice1/json-response1` というパスにマッチする
    # 2. v_json_practice.py ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonResponse1' %} のような形でURLを取得するのに使える

    # | Vuetify練習
    # +----




    # +----
    # | JSONでの応答練習

    # JSONでの応答練習
    path('json-practice/textarea2',
         # ----------------------
         # 1
         v_json_practice.readJsonTextarea2, name='readJsonTextarea2'),
    #    ---------------------------------        -----------------
    #    2                                        3
    # 1. URLの `json-practice/textarea2` というパスにマッチする
    # 2. v_json_practice.py ファイルの readJsonTextarea2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea2' %} のような形でURLを取得するのに使える

    # JSONでの応答練習
    path('json-practice/data-table2o3',
         # --------------------------
         # 1
         v_json_practice.readDataTable2o3, name='readDataTable2o3'),
    #    --------------------------------        ----------------
    #    2                                       3
    # 1. URLの `json-practice/data-table2o3` というパスにマッチする
    # 2. v_json_practice.py ファイルの readDataTable2o3 メソッド
    # 2. HTMLテンプレートの中で {% url 'readDataTable2o3' %} のような形でURLを取得するのに使える

    # | JSONでの応答練習
    # +----




    # +----
    # | 〇×ゲームの練習１

    # 対局要求
    path('tic-tac-toe/v1/match-request/', v_tic_tac_toe_v1.visitMatchRequest),
    #     -----------------------------   ----------------------------------
    #     1                               2
    # 1. URLの `tic-tac-toe/v1/match-request/` というパスにマッチする
    # 2. v_tic_tac_toe_v1.py ファイルの visitMatchRequest メソッド

    # 対局中
    path('tic-tac-toe/v1/play/<str:room_name>/', v_tic_tac_toe_v1.visitPlay),
    #     ------------------------------------   --------------------------
    #     1                                      2
    # 1. URLの `tic-tac-toe/v1/play/<部屋名>/` というパスにマッチする。 <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. v_tic_tac_toe_v1.py ファイルの visitPlay メソッド

    # | 〇×ゲームの練習１
    # +----




    # +----
    # | 〇×ゲームの練習２

    # 対局要求
    path('tic-tac-toe/v2/match-request/', v_tic_tac_toe_v2.visitMatchRequest),
    #                  ^                                 ^
    #     -----------------------------   ----------------------------------
    #     1                               2
    # 1. URLの `tic-tac-toe/v2/match-request/` というパスにマッチする
    # 2. v_tic_tac_toe_v2.py ファイルの visitMatchRequest メソッド

    # 対局中
    path('tic-tac-toe/v2/play/<str:room_name>/', v_tic_tac_toe_v2.visitPlay),
    #                  ^                                        ^
    #     ------------------------------------   --------------------------
    #     1                                      2
    # 1. URLの `tic-tac-toe/v2/play/<部屋名>/` というパスにマッチする。 <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. v_tic_tac_toe_v2.py ファイルの visitPlay メソッド

    # | 〇×ゲームの練習２
    # +----




    # +----
    # | 部屋

    # 部屋一覧
    path('rooms/', v_room.listRoom, name='listRoom'),
    #     ------   ---------------        ----------
    #     1        2                      3
    # 1. URLの `rooms/` というパスにマッチする
    # 2. v_room.py ファイルの listRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'listRoom' %} のような形でURLを取得するのに使える

    # 部屋読取
    path('rooms/read/<int:id>/', v_room.readRoom, name='readRoom'),
    #     --------------------   ---------------        ----------
    #     1                      2                      3
    # 1. URLの `rooms/read/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_room.py ファイルの readRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'readRoom' %} のような形でURLを取得するのに使える

    # 部屋削除
    path('rooms/delete/<int:id>/',
         # ------------------------
         # 1
         v_room.deleteRoom, name='deleteRoom'),
    #   ---------------------        ------------
    #   2                            3
    # 1. URLの `rooms/delete/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_room.py ファイルの deleteRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'deleteRoom' %} のような形でURLを取得するのに使える

    # 部屋作成
    path('rooms/create/', v_room.upsertRoom, name='createRoom'),
    #     -------------   -----------------        ----------
    #     1               2                        3
    # 1. URLの `rooms/create/` というパスにマッチする
    # 2. v_room.py ファイルの upsertRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'createRoom' %} のような形でURLを取得するのに使える

    # 部屋更新
    path('rooms/update/<int:id>/',
         # ---------------------
         # 1
         v_room.upsertRoom, name='updateRoom'),
    #    -----------------        ----------
    #    2                        3
    # 1. URLの `rooms/update/<数字列>/` というパスにマッチする。数字列は views.py の中で id という名前で取得できる
    # 2. v_room.py ファイルの upsertRoom メソッド
    # 3. HTMLテンプレートの中で {% url 'updateRoom' %} のような形でURLを取得するのに使える

    # | 部屋
    # +----




    # +----
    # | ポータル作成

    # 旧ポータル
    path('tic-tac-toe2/', v_tic_tac_toe_v2o1.visitPortal,
         # ------------   ------------------------------
         # 1             2
         name='visitTicTacToeV2Portal'),
    #          ----------------------
    #          3
    # 1. URLの `tic-tac-toe2/` というパスにマッチする
    # 2. v_tic_tac_toe_v2o1.py ファイルの visitPortal メソッド
    # 3. HTMLテンプレートの中で {% url 'visitTicTacToeV2Portal' %} のような形でURLを取得するのに使える

    # ポータル
    path('tic-tac-toe/v2/', v_tic_tac_toe_v2o1.visitPortal,
         # --------------   ------------------------------
         # 1                2
         name='visitTicTacToeV2Portal'),
    #          ----------------------
    #          3
    # 1. URLの `tic-tac-toe/v2/` というパスにマッチする
    # 2. v_tic_tac_toe_v2o1.py ファイルの visitPortal メソッド
    # 3. HTMLテンプレートの中で {% url 'visitTicTacToeV2Portal' %} のような形でURLを取得するのに使える

    # ログイン
    path('tic-tac-toe/v2/login/', v_tic_tac_toe_v2o1.loginUser,
         # --------------------   ----------------------------
         # 1                      2
         name='ticTacToeV2o1_loginUser'),
    #          ----------------------
    #          3
    # 1. URLの `login/tic-tac-toe/v2/` というパスにマッチする
    # 2. v_tic_tac_toe_v2o1.py ファイルの loginUser メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2o1_loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('tic-tac-toe/v2/logout/', v_tic_tac_toe_v2o1.logoutUser,
         # ---------------------   -----------------------------
         # 1                       2
         name='ticTacToeV2o1_logout'),
    #          -------------------
    #          3
    # 1. URLの `tic-tac-toe/v2/logout/` というパスにマッチする
    # 2. v_tic_tac_toe_v2o1.py ファイルの logoutUser メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2o1_logout' %} のような形でURLを取得するのに使える

    # | ポータル作成
    # +----



    # +----
    # | ホーム

    # ポータル
    path('home/v2/', v_home_v2.visitHome, name='homeV2VisitHome'),
    #     --------   -------------------        ---------------
    #     1          2                          3
    #
    # 1. URLの `home/v2/` というパスにマッチする
    # 2. v_home_v2.py ファイルの visitHome メソッド
    # 3. HTMLテンプレートの中で {% url 'homeV2VisitHome' %} のような形でURLを取得するのに使える

    # | ホーム
    # +----




    # +----
    # | ロビー（待合室）

    # ロビー（待合室）
    path('lobby/v1/', v_lobby_v1.visitLobby, name='lobbyV1VisitLobby'),
    #     ---------   ---------------------        -----------------
    #     1           2                            3
    #
    # 1. URLの `lobby/v1/` というパスにマッチする
    # 2. v_lobby_v1.py ファイルの visitLobby メソッド
    # 3. HTMLテンプレートの中で {% url 'lobbyV1VisitLobby' %} のような形でURLを取得するのに使える

    # | ロビー（待合室）
    # +----




    # +----
    # | WIP

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

    # | WIP
    # +----
]


def grpc_handlers(server):
    account_pb2_grpc.add_UserControllerServicer_to_server(
        UserService.as_servicer(), server)
