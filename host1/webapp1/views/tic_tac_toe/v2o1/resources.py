"""〇×ゲームの練習２．１"""
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


class Portal():
    """ポータル"""

    _path_of_html = "webapp1/tic-tac-toe/v2/portal.html"
    #                ----------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/portal.html を取得
    #                            ----------------------------------

    _path_of_match_application = "/tic-tac-toe/v2/match-application/"
    #                             ----------------------------------
    #                             1
    # 1. http://example.com/tic-tac-toe/v2/match-application/
    #                      ----------------------------------

    _path_of_signin = "/tic-tac-toe/v2/login/"
    #                  ----------------------
    #                  1
    # 1. http://example.com/tic-tac-toe/v2/login/
    #                      ----------------------

    _path_of_signout = "/tic-tac-toe/v2/logout/"
    #                   -----------------------
    #                   1
    # 1. http://example.com/tic-tac-toe/v2/logout/
    #                      -----------------------

    @staticmethod
    def render(request):
        """描画"""
        return portal_render(request, Portal._path_of_html, Portal._path_of_match_application, Portal._path_of_signin, Portal._path_of_signout)


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


def portal_render(request, path_of_html, path_of_match_application, path_of_signinin, path_of_signout):
    """ポータル - 描画"""
    template = loader.get_template(path_of_html)

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,
        'dj_pathOfMatchApplication': path_of_match_application,
        'dj_pathOfSignin': path_of_signinin,
        'dj_pathOfLogout': path_of_signout,
    }
    return HttpResponse(template.render(context, request))


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
