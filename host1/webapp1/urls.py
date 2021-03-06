from django.contrib import admin
from django.urls import path
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

from webapp1.views import v_login_user, v_member, \
    v_room, v_home, v_lobby_v1

from webapp1.views.practice import pages as practice_pages
#    ------- --------------        -----    --------------
#    1       2                     3        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.practice import json as practice_json
#    ------- --------------        ----    -------------
#    1       2                     3       4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.practice import session as practice_session
#    ------- --------------        -------    ----------------
#    1       2                     3          4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.practice import vuetify as practice_vuetify
#    ------- --------------        -------    ----------------
#    1       2                     3          4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v2 import resources as tic_tac_toe_v2
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v2o1 import resources as tic_tac_toe_v2o1
#    ------- ----------------------        ---------    ----------------
#    1       2                             3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v3 import resources as tic_tac_toe_v3
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v3o1 import resources as tic_tac_toe_v3o1
#    ------- ----------------------        ---------    ----------------
#    1       2                             3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v3o2 import resources as tic_tac_toe_v3o2
#    ------- ----------------------        ---------    ----------------
#    1       2                             3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [

    # +----
    # | ポータル

    # ポータル
    path('', v_index.render_index, name='index'),
    #    --  --------------------        -----
    #    1   2                           3
    # 1. 例えば `http://example.com/` のように、 URLのパスの部分を指定しなかったケースに対応します
    # 2. v_index.py ファイルの render_index メソッド
    # 3. HTMLテンプレートの中で {% url 'index' %} のような形でURLを取得するのに使える

    # | ポータル
    # +----




    # +----
    # | 管理者

    # 管理画面
    path('admin/', admin.site.urls),
    #     ------   ---------------
    #     1        2
    # 1. 例えば `http://example.com/admin/` のような URLのパスの部分
    # 2. django に用意されている管理画面のパスを 1. のパスにぶら下げる形で全てコピーします

    # | 管理者
    # +----




    # +----
    # | 認証

    # https://sinyblog.com/django/django-allauth/
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #    --  -----------------------------------------------        ----
    #    1   2                                                      3
    # 1. URL に パスを付けなかったときにマッチする
    # 2. 最初から用意されているページ？
    # 3. ログイン後に飛んでくるページの URL のパスを 'home' という名前で覚えておく

    # | 認証
    # +----




    # +----
    # | ログイン/ログアウト

    # ログイン
    path('login-user', v_login_user.LoggingIn.render, name='loginUser'),
    #     ----------   -----------------------------        ---------
    #     1            2                                    3
    # 1. 例えば `http://example.com/login-user` のような URL のパスの部分
    #                              -----------
    # 2. v_login_user.py ファイルの LoggingIn クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('logout', v_login_user.LoggingOut.render, name='logoutUser'),
    #     ------   ------------------------------        ----------
    #     1        2                                     3
    # 1. 例えば `http://example.com/logout` のような URL のパスの部分
    #                              -------
    # 2. v_login_user.py ファイルの LoggingOut クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'logoutUser' %} のような形でURLを取得するのに使える

    # | ログイン
    # +----




    # +----
    # | 会員

    # 会員一覧
    path('members/', v_member.listMember, name='listMember'),
    #     --------   -------------------        ----------
    #     1          2                          3
    # 1. 例えば `http://example.com/members/` のような URL のパスの部分
    #                              ---------
    # 2. v_member.py ファイルの listMember メソッド
    # 3. HTMLテンプレートの中で {% url 'listMember' %} のような形でURLを取得するのに使える

    # 会員読取
    path('members/read/<int:id>/',
         # ---------------------
         # 1
         v_member.readMember, name='readMember'),
    #    -------------------        ----------
    #    2                          3
    # 1. 例えば `http://example.com/members/read/<数字列>/` のような URL のパスの部分。数字列は v_member.py の中で id という名前で取得できる
    #                              ----------------------
    # 2. v_member.py ファイルの readMember メソッド
    # 3. HTMLテンプレートの中で {% url 'readMember' %} のような形でURLを取得するのに使える

    # 会員削除
    path('members/delete/<int:id>/',
         # ------------------------
         # 1
         v_member.deleteMember, name='deleteMember'),
    #   ---------------------        ------------
    #   2                            3
    # 1. 例えば `http://example.com/members/delete/<数字列>/` のような URL のパスの部分。数字列は v_member.py の中で id という名前で取得できる
    #                              ------------------------
    # 2. v_member.py ファイルの deleteMember メソッド
    # 3. HTMLテンプレートの中で {% url 'deleteMember' %} のような形でURLを取得するのに使える

    # 会員作成
    path('members/create/', v_member.upsertMember, name='createMember'),
    #     ---------------   ---------------------        ------------
    #     1                 2                            3
    # 1. 例えば `http://example.com/members/create/` のような URL のパスの部分
    #                              ----------------
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'createMember' %} のような形でURLを取得するのに使える

    # 会員更新
    path('members/update/<int:id>/',
         # -----------------------
         # 1
         v_member.upsertMember, name='updateMember'),
    #    ---------------------        ------------
    #    2                            3
    # 1. 例えば `http://example.com/members/update/<数字列>/` のような URL のパスの部分。数字列は v_member.py の中で id という名前で取得できる
    #                              ------------------------
    # 2. v_member.py ファイルの upsertMember メソッド
    # 3. HTMLテンプレートの中で {% url 'updateMember' %} のような形でURLを取得するのに使える

    # | 会員
    # +----




    # +----
    # | 練習

    # Vuetify練習
    path('practice/vuetify-data-table2o2', practice_vuetify.readDataTable2o2,
         # -----------------------------   ---------------------------------
         # 1                               2
         name='readDataTable2o2'),
    #          ----------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-data-table2o2` のような URL のパスの部分
    #                              -------------------------------
    # 2. practice_vuetify (別名)ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2o2' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/json-response1',
         # ----------------------
         # 1
         practice_json.readJsonResponse1, name='readJsonResponse1'),
    #    -------------------------------        -----------------
    #    2                                      3
    # 1. 例えば `http://example.com/practice/json-response1` のような URL のパスの部分
    #                              ------------------------
    # 2. practice_json (別名)ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonResponse1' %} のような形でURLを取得するのに使える

    # JSONでの応答練習
    path('practice/json-textarea2',
         # ----------------------
         # 1
         practice_json.readJsonTextarea2, name='readJsonTextarea2'),
    #    -------------------------------        -----------------
    #    2                                      3
    # 1. 例えば `http://example.com/practice/json-textarea2` のような URL のパスの部分
    #                              ------------------------
    # 2. practice_json (別名)ファイルの readJsonTextarea2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea2' %} のような形でURLを取得するのに使える

    # JSONでの応答練習
    path('practice/json-data-table2o3',
         # --------------------------
         # 1
         practice_json.readDataTable2o3, name='readDataTable2o3'),
    #    ------------------------------        ----------------
    #    2                                          3
    # 1. 例えば `http://example.com/practice/json-data-table2o3` のような URL のパスの部分
    #                              ---------------------------
    # 2. practice_json (別名)ファイルの readDataTable2o3 メソッド
    # 2. HTMLテンプレートの中で {% url 'readDataTable2o3' %} のような形でURLを取得するのに使える

    # | 練習
    # +----




    # +----
    # | 〇×ゲーム２

    # 対局申込
    path('tic-tac-toe/v2/match-application/',
         #             ^
         # --------------------------------
         # 1
         tic_tac_toe_v2.MatchApplication.render),
    #                   ^
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/match-application/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v2 (別名)ファイルの MatchApplication クラスの render 静的メソッド

    # 対局中
    path('tic-tac-toe/v2/playing/<str:kw_room_name>/',
         #             ^
         # -----------------------------------------
         # 1
         tic_tac_toe_v2.Playing.render),
    #                 ^
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/playing/<部屋名>/` のような URL のパスの部分。
    #                              --------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v2 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム２
    # +----




    # +----
    # | 〇×ゲーム３

    # 対局申込
    path('tic-tac-toe/v3/match-application/',
         #             ^
         # --------------------------------
         # 1
         tic_tac_toe_v3.MatchApplication.render),
    #                 ^
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/match-application/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v3.py (別名)ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3/playing/<str:kw_room_name>/',
         #             ^
         # -----------------------------------------
         # 1
         tic_tac_toe_v3.Playing.render),
    #                 ^
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3/playing/<部屋名>/` のような URL のパスの部分。
    #                              --------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v3.py (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３
    # +----




    # +----
    # | 〇×ゲーム３．１

    # 対局申込
    path('tic-tac-toe/v3o1/match-application/',
         #             ^^^
         # ----------------------------------
         # 1
         tic_tac_toe_v3o1.MatchApplication.render),
    #                 ^^^
    #    ----------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. tic_tac_toe_v3o1 (別名)ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3o1/playing/<str:kw_room_name>/',
         #             ^^^
         # -------------------------------------------
         # 1
         tic_tac_toe_v3o1.Playing.render),
    #                 ^^^
    #    -------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o1/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v3o1 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３．１
    # +----




    # +----
    # | 〇×ゲーム３．２

    # 対局申込
    path('tic-tac-toe/v3o2/match-application/',
         #             ^^^ three o two
         # ----------------------------------
         # 1
         tic_tac_toe_v3o2.MatchApplication.render),
    #                 ^^^ three o two
    #    ----------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o2/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. tic_tac_toe_v3o2 (別名)ファイルの MatchApplication クラスの render メソッド

    # 対局中
    path('tic-tac-toe/v3o2/playing/<str:kw_room_name>/',
         #             ^^^ three o two
         # -------------------------------------------
         # 1
         tic_tac_toe_v3o2.Playing.render),
    #                 ^^^
    #    -------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v3o2/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v3o2 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム３．２
    # +----




    # +----
    # | ポータル作成

    # 旧ポータル
    path('tic-tac-toe2/', tic_tac_toe_v2o1.Portal.render,
         # ------------   ------------------------------
         # 1              2
         name='ticTacToeV2_portal'),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe2/` のような URL のパスの部分
    #                              --------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの Portal クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2_portal' %} のような形でURLを取得するのに使える

    # ポータル
    path('tic-tac-toe/v2/', tic_tac_toe_v2o1.Portal.render,
         # --------------   ------------------------------
         # 1                2
         name='ticTacToeV2_portal'),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe/v2/` のような URL のパスの部分
    #                              ----------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの Portal クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2_portal' %} のような形でURLを取得するのに使える

    # ログイン
    path('tic-tac-toe/v2/login/', tic_tac_toe_v2o1.LoggingIn.render,
         # --------------------   ---------------------------------
         # 1                      2
         name='ticTacToeV2o1_loginUser'),
    #          -----------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe/v2/login/` のような URL のパスの部分
    #                              ----------------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの LoggingIn クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2o1_loginUser' %} のような形でURLを取得するのに使える

    # ログアウト
    path('tic-tac-toe/v2/logout/', tic_tac_toe_v2o1.LoggingOut.render,
         # ---------------------   ----------------------------------
         # 1                       2
         name='ticTacToeV2o1_logout'),
    #          --------------------
    #          3
    # 1. 例えば `http://example.com/tic-tac-toe/v2/logout/` のような URL のパスの部分
    #                              -----------------------
    # 2. tic_tac_toe_v2o1 (別名)ファイルの LoggingOut クラスの render 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'ticTacToeV2o1_logout' %} のような形でURLを取得するのに使える

    # | ポータル作成
    # +----



    # +----
    # | ホーム

    # ポータル
    path('home/v1/', v_home.render_home, name='homeV1_home'),
    #     --------   ------------------        -----------
    #     1          2                         3
    #
    # 1. 例えば `http://example.com/home/v1/` のような URL のパスの部分
    #                              ---------
    # 2. v_home.py ファイルの render_home メソッド
    # 3. HTMLテンプレートの中で {% url 'homeV1_home' %} のような形でURLを取得するのに使える

    # | ホーム
    # +----




    # +----
    # | ロビー（待合室）

    # ロビー（待合室）
    path('lobby/v1/', v_lobby_v1.render_lobby, name='lobbyV1_lobby'),
    #     ---------   -----------------------        -------------
    #     1           2                              3
    #
    # 1. 例えば `http://example.com/lobby/v1/` のような URL のパスの部分
    #                              ----------
    # 2. v_lobby_v1.py ファイルの render_lobby メソッド
    # 3. HTMLテンプレートの中で {% url 'lobbyV1_lobby' %} のような形でURLを取得するのに使える

    # | ロビー（待合室）
    # +----
]


def grpc_handlers(server):
    account_pb2_grpc.add_UserControllerServicer_to_server(
        UserService.as_servicer(), server)
