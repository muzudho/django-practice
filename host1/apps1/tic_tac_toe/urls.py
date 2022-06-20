from django.urls import path

# 〇×ゲームの練習１
from apps1.tic_tac_toe.views.v1o1 import resources as tic_tac_toe_v1
#    ----- ----------- ----------        ---------    --------------
#    1     2           3                 4            5
#    ----------------------------
#    6
# 1. 開発者用ディレクトリーの一部
# 2. アプリケーション フォルダー名
# 3. ディレクトリー名
# 4. Python ファイル名。拡張子抜き
# 5. `4.` の別名
# 6. モジュール名

# 〇×ゲームの練習２．０．１
from apps1.tic_tac_toe.views.v2o0o1 import resources as tic_tac_toe_v2o0o1
#    ----- ----------- ------------        ---------    ------------------
#    1     2           3                   4            5
#    ------------------------------
#    6
# 1. 開発者用ディレクトリーの一部
# 2. アプリケーション フォルダー名
# 3. ディレクトリー名
# 4. Python ファイル名。拡張子抜き
# 5. `4.` の別名
# 6. モジュール名


urlpatterns = [

    # +----
    # | 〇×ゲーム１

    # 対局申込
    path('tic-tac-toe/v1o1/match-application/',
         # ----------------------------------
         # 1
         tic_tac_toe_v1.MatchApplication.render),
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v1o1/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. tic_tac_toe_v1 (別名)ファイルの MatchApplication クラスの render 静的メソッド

    # 対局中
    path('tic-tac-toe/v1o1/playing/<str:room_name>/',
         # ----------------------------------------
         # 1
         tic_tac_toe_v1.Playing.render),
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v1o1/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. tic_tac_toe_v1 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム１
    # +----




    # +----
    # | 〇×ゲーム２．０．１

    # 対局申込
    path('tic-tac-toe/v2o0o1/engine-manual/',
         #             ^^^^^ two o zero o one
         # --------------------------------
         # 1
         tic_tac_toe_v2o0o1.EngineManual.render),
    #                 ^^^^^ two o zero o one
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v2o0o1/engine-manual/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v2o0o1 (別名)ファイルの EngineManual クラスの render 静的メソッド

    # | 〇×ゲーム２．０．１
    # +----

]
