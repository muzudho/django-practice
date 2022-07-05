"""〇×ゲームの練習２．１"""
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


class LoggingIn():
    """ログイン中"""

    _path_of_http_playing = "/tic-tac-toe/v2/playing/{0}/?&myturn={1}"
    #                                      ^ two
    #                        ----------------------------------------
    #                        1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&myturn=X
    #                           -------------------------------------------

    _path_of_match_application = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                                  ^ two
    #                             ---------------------------------------------
    #                             1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    # 👇 このデコレーターを付けると、ログインしていないなら、 settings.py の LOGIN_URL で指定した URL に飛ばします。
    # インスタンスのメソッドや、クラスメソッドには付けられません。
    # 第一引数が self や clazz でないことに注意してください
    @login_required
    def render(request):
        """描画"""
        return logging_in_render(request, LoggingIn._path_of_http_playing, LoggingIn._path_of_match_application)


class LoggingOut():
    """ログアウト中"""

    @staticmethod
    def render(request):
        """描画"""
        return logging_out_render(request)


# 以下、関数


def logging_in_render(request, path_of_http_playing, path_of_match_application):
    """ログイン中 - 描画"""
    if request.method == "POST":
        # 送信後

        # `po_` は POST送信するパラメーター名の目印
        room_name = request.POST.get("po_room_name")
        my_turn = request.POST.get("po_my_turn")

        return redirect(path_of_http_playing.format(room_name, my_turn))

    # 訪問後
    return render(request, path_of_match_application, {})


def logging_out_render(request):
    """ログアウト中 - 描画"""

    logout(request)  # Django の認証機能のログアウトを使う

    return redirect('ticTacToeV2_portal')  # ホームに戻る
