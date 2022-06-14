"""〇×ゲームの練習３．２"""
import json
from webapp1.views.tic_tac_toe.v2 import resources as tic_tac_toe_v2
#                               ^ two                              ^ two
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

from webapp1.views.tic_tac_toe.v3 import resources as tic_tac_toe_v3
#                               ^ three                            ^ three
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名


# 以下、よく使う定型データ


# 対局申込 - 訪問後
match_application_open_context = {
    # `dj_` は Djangoでレンダーするパラメーター名の目印
    # 入場者データ
    "dj_visitor_value": "X",
    # Python と JavaScript 間で配列データを渡すために JSON 文字列形式にします
    "dj_visitor_select": json.dumps([
        {"text": "X", "value": "X"},
        {"text": "O", "value": "O"},
        {"text": "WatchingGame", "value": "_"},  # add
    ]),
}


# 対局中 - 駒
playing_expected_pieces = ['X', 'O', '_']


# 以下、ロジック


class MatchApplication():
    """対局申込ページ"""

    _path_of_http_playing = "/tic-tac-toe/v3o2/playing/{0}/?&mypiece={1}"
    #                                    ^^^ three o two
    #                      -------------------------------------------
    #                      1
    # 1. http://example.com:8000/tic-tac-toe/v3o1/playing/Elephant/?&mypiece=X
    #                           ----------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                     ^ two
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        return tic_tac_toe_v2.render_match_application(request, MatchApplication._path_of_http_playing, MatchApplication._path_of_html, MatchApplication.on_sent, MatchApplication.open)
        #                   ^ two

    @staticmethod
    def on_sent(request):
        """送信後"""
        return tic_tac_toe_v3.match_application_on_sent(request)
        #                   ^ three

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return match_application_open_context
        #      ^ Located in this file


class Playing():

    _path_of_ws_playing = "/tic-tac-toe/v3o1/playing/"
    #                                    ^^^ three o one
    #                      --------------------------
    #                      1
    # 1. ws://example.com/tic-tac-toe/v3o1/playing/Elephant/
    #                    --------------------------

    _path_of_html = "webapp1/tic-tac-toe/v3o2/playing.html.txt"
    #                                     ^ three o two
    #                -----------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3o2/playing.html.txt
    #                            -----------------------------------------

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        return tic_tac_toe_v2.render_playing(
            #               ^ two
            request,
            kw_room_name,
            Playing._path_of_ws_playing,
            Playing._path_of_html,
            Playing.on_update,
            playing_expected_pieces)
        #   ^ Located in this file

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass
