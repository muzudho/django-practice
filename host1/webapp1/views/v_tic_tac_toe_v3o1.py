from webapp1.views.v_tic_tac_toe_v3 import MatchApplication as MatchApplicationV3
#    ------- ----- ----------------        ----------------    ------------------
#    1       2     3                       4                   5
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名
# 5. `4.` に付けた別名

from webapp1.views.v_tic_tac_toe_v3 import Playing as PlayingV3
#    ------- ----- ----------------        -------    ---------
#    1       2     3                       4          5
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名
# 5. `4.` に付けた別名


class MatchApplication(MatchApplicationV3):
    """対局申込ページ"""

    _path_of_playing = "/tic-tac-toe/v3o1/playing/{0}/?&mypiece={1}"
    #                                 ^^^ three o one
    #                   -------------------------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v3o1/playing/Elephant/?&mypiece=X
    #                           ----------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                     ^ two
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------


class Playing(PlayingV3):

    _path_of_playing = "/tic-tac-toe/v3o1/playing/"
    #                                 ^^^ three o one
    #                   --------------------------
    #                   1
    # 1. http://example.com/tic-tac-toe/v3o1/playing/Elephant/
    #                      --------------------------
