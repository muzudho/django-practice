"""〇×ゲームの練習３．１"""
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


class MatchApplication():
    """対局申込ページ"""

    _path_of_http_playing = "/tic-tac-toe/v3o1/playing/{0}/?&mypiece={1}"
    #                                      ^^^ three o one
    #                        -------------------------------------------
    #                        1
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

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return tic_tac_toe_v2.match_application_open_context
        #                   ^ two


class Playing():

    _path_of_ws_playing = "/tic-tac-toe/v3o1/playing/"
    #                                    ^^^ three o one
    #                      --------------------------
    #                      1
    # 1. ws://example.com/tic-tac-toe/v3o1/playing/Elephant/
    #                    --------------------------

    _path_of_html = "webapp1/tic-tac-toe/v3/playing.html.txt"
    #                                     ^ three
    #                ---------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/playing.html.txt
    #                            ---------------------------------------

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        return tic_tac_toe_v2.render_playing(request, kw_room_name, Playing._path_of_ws_playing, Playing._path_of_html, Playing.on_update)
        #                   ^ two

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass
