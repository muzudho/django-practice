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

from webapp1.views import v_login_user, v_practice_of_pages, v_member, v_practice_of_vuetify, \
    v_practice_of_json, \
    v_room, v_home, v_lobby_v1, v_practice_of_session, v_accounts_v1, v_practice

from webapp1.views.tic_tac_toe.v1 import resources as tic_tac_toe_v1
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
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

    # allauth の URLのパスのコピー
    path('accounts/v1/', include('allauth.urls')),
    #     ------------   -----------------------
    #     1
    # 1. 例えば `http://example.com/accounts/v1/` のような URLのパスの部分
    # 2. allauth の例えば `login/` のようなパスを 1. のパスにぶら下げる形で全てコピーします

    # サインアップ（会員登録）
    path("accounts/v1/signup/", view=v_accounts_v1.accounts_v1_signup_view,
         # ------------------        -------------------------------------
         # 1                        2
         name="accounts_v1_signup"),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/accounts/v1/signup/` のような URL のパスの部分
    #                              -------------------
    # 2. allauth の SignupView をカスタマイズしたオブジェクト
    # 3. HTMLテンプレートの中で {% url 'accounts_v1_signup' %} のような形でURLを取得するのに使える

    # サインイン
    path("accounts/v1/login/", view=v_accounts_v1.accounts_v1_login_view,
         # -----------------        ------------------------------------
         # 1                        2
         name="accounts_v1_login"),
    #          -----------------
    #          3
    # 1. 例えば `http://example.com/accounts/v1/login/` のような URL のパスの部分
    #                              -------------------
    # 2. 既に用意されているビューのオブジェクト？
    # 3. HTMLテンプレートの中で {% url 'accounts_v1_login' %} のような形でURLを取得するのに使える

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
    # | 練習１

    # ページ１
    path('practice/page1', v_practice_of_pages.render_page1, name='page1'),
    #     --------------   --------------------------------        -----
    #     1                2                                       3
    # 1. 例えば `http://example.com/practice/page1` のような URL のパスの部分
    #                              ---------------
    # 2. v_practice_of_pages.py ファイルの render_page1 メソッド
    # 3. HTMLテンプレートの中で {% url 'page1' %} のような形でURLを取得するのに使える

    # ページ２の第１，２区画
    path('practice/page2_1o2',
         # -----------------
         # 1
         v_practice_of_pages.render_page2_section1o2, name='page1'),
    #    -------------------------------------------        -----
    #    2                                                  3
    # 1. URLの `practice/page2_1o2` というパスにマッチする
    # 2. v_practice_of_pages.py ファイルの render_page2_section1o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'page1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/vuetify-hello1',
         # ----------------------
         # 1
         v_practice_of_vuetify.readHello, name='readHello'),
    #    -------------------------------        ---------
    #    2                                      3
    # 1. 例えば `http://example.com/practice/vuetify-hello1` のような URL のパスの部分
    #                              ------------------------
    # 2. v_practice_of_vuetify.py ファイルの readHello メソッド
    # 3. HTMLテンプレートの中で {% url 'readHello' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/vuetify-data-table1', v_practice_of_vuetify.readDataTable1,
         # ---------------------------   ------------------------------------
         # 1                             2
         name='readDataTable1'),
    #          --------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-data-table1` のような URL のパスの部分
    #                              -----------------------------
    # 2. v_practice_of_vuetify.py ファイルの readDataTable1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/vuetify-data-table2', v_practice_of_vuetify.readDataTable2,
         # ---------------------------   ------------------------------------
         # 1                             2
         name='readDataTable2'),
    #          --------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-data-table2` のような URL のパスの部分
    #                              -----------------------------
    # 2. v_practice_of_vuetify.py ファイルの readDataTable2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2' %} のような形でURLを取得するのに使える

    # Vuetifyのテキストフィールドのバリデーションの練習
    path('practice/vuetify-text-field-validation1', v_practice_of_vuetify.render_practice_text_field_validation1,
         # --------------------------------------   ------------------------------------------------------------
         # 1                                        2
         name='practice_text_field_validation1'),
    #          -------------------------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-text-field-validation1` のような URL のパスの部分
    #                              ---------------------------------------
    # 2. v_practice_of_vuetify.py ファイルの render_practice_text_field_validation1 メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_text_field_validation1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/vuetify-json-textarea1', v_practice_of_vuetify.readJsonTextarea1,
         # ------------------------------   ---------------------------------------
         # 1                                2
         name='readJsonTextarea1'),
    #          -----------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-json-textarea1` のような URL のパスの部分
    #                              -------------------------------
    # 2. v_practice_of_vuetify.py ファイルの readJsonTextarea1 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/vuetify-data-table2o2', v_practice_of_vuetify.readDataTable2o2,
         # -----------------------------   --------------------------------------
         # 1                               2
         name='readDataTable2o2'),
    #          ----------------
    #          3
    # 1. 例えば `http://example.com/practice/vuetify-data-table2o2` のような URL のパスの部分
    #                              -------------------------------
    # 2. v_practice_of_vuetify.py ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readDataTable2o2' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('practice/json-response1',
         # ----------------------
         # 1
         v_practice_of_json.readJsonResponse1, name='readJsonResponse1'),
    #    ------------------------------------        -----------------
    #    2                                           3
    # 1. 例えば `http://example.com/practice/json-response1` のような URL のパスの部分
    #                              ------------------------
    # 2. v_practice_of_json.py ファイルの readDataTable2o2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonResponse1' %} のような形でURLを取得するのに使える

    # JSONでの応答練習
    path('practice/json-textarea2',
         # ----------------------
         # 1
         v_practice_of_json.readJsonTextarea2, name='readJsonTextarea2'),
    #    ------------------------------------        -----------------
    #    2                                           3
    # 1. 例えば `http://example.com/practice/json-textarea2` のような URL のパスの部分
    #                              ------------------------
    # 2. v_practice_of_json.py ファイルの readJsonTextarea2 メソッド
    # 3. HTMLテンプレートの中で {% url 'readJsonTextarea2' %} のような形でURLを取得するのに使える

    # JSONでの応答練習
    path('practice/json-data-table2o3',
         # --------------------------
         # 1
         v_practice_of_json.readDataTable2o3, name='readDataTable2o3'),
    #    -----------------------------------        ----------------
    #    2                                          3
    # 1. 例えば `http://example.com/practice/json-data-table2o3` のような URL のパスの部分
    #                              ---------------------------
    # 2. v_practice_of_json.py ファイルの readDataTable2o3 メソッド
    # 2. HTMLテンプレートの中で {% url 'readDataTable2o3' %} のような形でURLを取得するのに使える

    # | 練習
    # +----




    # +----
    # | 〇×ゲーム１

    # 対局申込
    path('tic-tac-toe/v1/match-application/',
         # --------------------------------
         # 1
         tic_tac_toe_v1.MatchApplication.render),
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v1/match-application/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v1 (別名)ファイルの MatchApplication クラスの render 静的メソッド

    # 対局中
    path('tic-tac-toe/v1/playing/<str:room_name>/',
         # --------------------------------------
         # 1
         tic_tac_toe_v1.Playing.render),
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v1/playing/<部屋名>/` のような URL のパスの部分。
    #                              --------------------------------
    #    <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. tic_tac_toe_v1 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム１
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
    # | 部屋

    # 一覧
    path('rooms/', v_room.RoomView.render_list, name='listRoom'),
    #     ------   ---------------------------        ----------
    #     1        2                                  3
    # 1. 例えば `http://example.com/rooms/` のような URL のパスの部分
    #                              -------
    # 2. v_room.py ファイルの RoomView クラスの render_list 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'listRoom' %} のような形でURLを取得するのに使える

    # 読取
    path('rooms/read/<int:id>/', v_room.RoomView.render_read, name='readRoom'),
    #     --------------------   ---------------------------        ----------
    #     1                      2                                  3
    # 1. 例えば `http://example.com/rooms/read/<数字列>/` のような URL のパスの部分。数字列は v_room.py の中で id という名前で取得できる
    #                              --------------------
    # 2. v_room.py ファイルの RoomView クラスの render_read 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'readRoom' %} のような形でURLを取得するのに使える

    # 削除
    path('rooms/delete/<int:id>/',
         # ---------------------
         # 1
         v_room.RoomView.render_delete, name='deleteRoom'),
    #    -----------------------------        ----------
    #    2                                    3
    # 1. 例えば `http://example.com/rooms/delete/<数字列>/` のような URL のパスの部分
    #                              ----------------------
    #    数字列は v_room.py の中で id という名前で取得できる
    # 2. v_room.py ファイルの RoomView クラスの render_delete 静的メソッド
    # 3. HTMLテンプレートの中で {% url 'deleteRoom' %} のような形でURLを取得するのに使える

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
    # | セッション練習

    # アクティブ ユーザー一覧
    path('practice/session-active-user-list/',
         # ------------------------------------
         # 1
         v_practice_of_session.render_active_user_list, name='sessionPracticeV1_activeUserList'),
    #    ---------------------------------------------        --------------------------------
    #    2                                                    3
    #
    # 1. 例えば `http://example.com/practice/session-active-user-list/` のような URL のパスの部分
    #                              --------------------------------------
    # 2. v_practice_of_session.py ファイルの render_active_user_list メソッド
    # 3. HTMLテンプレートの中で {% url 'sessionPracticeV1_activeUserList' %} のような形でURLを取得するのに使える

    # | セッション練習
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




    # +----
    # | 練習

    # 会員登録ユーザー一覧
    path('practice/user-list/',
         # ------------------
         # 1
         v_practice.render_user_list, name='practice_userList'),
    #    ---------------------------        -----------------
    #    2                                  3
    #
    # 1. 例えば `http://example.com/practice/user-list/` のような URL のパスの部分
    #                              --------------------
    # 2. v_practice.py ファイルの render_user_list メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_userList' %} のような形でURLを取得するのに使える

    # 会員登録ユーザー一覧 v2
    path('practice/user-list/v2/',
         # ---------------------
         # 1
         v_practice.render_user_list_v2, name='practice_userListV2'),
    #    ------------------------------        -------------------
    #    2                                     3
    #
    # 1. 例えば `http://example.com/practice/user-list/v2/` のような URL のパスの部分
    #                              -----------------------
    # 2. v_practice.py ファイルの render_user_list_v2 メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_userListV2' %} のような形でURLを取得するのに使える

    # 対局待合室
    path('practice/waiting-for-match/',
         # --------------------------
         # 1
         v_practice.render_waiting_for_match, name='practice_waitingForMatch'),
    #    -----------------------------------        ------------------------
    #    2                                          3
    #
    # 1. 例えば `http://example.com/waiting-for-match/` のような URL のパスの部分
    #                              -------------------
    # 2. v_practice.py ファイルの render_waiting_for_match メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_waitingForMatch' %} のような形でURLを取得するのに使える

    # 対局待合室 v2
    path('practice/waiting-for-match/v2/',
         # -----------------------------
         # 1
         v_practice.render_waiting_for_match_v2, name='practice_waitingForMatchV2'),
    #    --------------------------------------        --------------------------
    #    2                                             3
    #
    # 1. 例えば `http://example.com/waiting-for-match/v2/` のような URL のパスの部分
    #                              ----------------------
    # 2. v_practice.py ファイルの render_waiting_for_match_v2 メソッド
    # 3. HTMLテンプレートの中で {% url 'practice_waitingForMatchV2' %} のような形でURLを取得するのに使える

    # | 練習
    # +----
]


def grpc_handlers(server):
    account_pb2_grpc.add_UserControllerServicer_to_server(
        UserService.as_servicer(), server)
