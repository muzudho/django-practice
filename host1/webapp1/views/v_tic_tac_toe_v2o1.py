from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


class Portal():
    """ポータル"""

    @staticmethod
    def render(request):
        """描画"""

        template = loader.get_template('webapp1/tic-tac-toe/v2/portal.html')
        #                               ----------------------------------
        #                               1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/portal.html を取得
        #                            ----------------------------------

        context = {
            # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
            'dj_user': request.user,
            'dj_pathOfMatchRequest': '/tic-tac-toe/v2/match-request/',
            #                         ------------------------------
            #                         1
            # 1. http://example.com/tic-tac-toe/v2/match-request/
            #                      ------------------------------
            'dj_pathOfSignin': '/tic-tac-toe/v2/login/',
            #                  ----------------------
            #                  1
            # 1. http://example.com/tic-tac-toe/v2/login/
            #                      ----------------------
            'dj_pathOfLogout': '/tic-tac-toe/v2/logout/',
            #                   -----------------------
            #                   1
            # 1. http://example.com/tic-tac-toe/v2/logout/
            #                      -----------------------
        }
        return HttpResponse(template.render(context, request))


@login_required  # 👈 このデコレーターを付けると、ログインしていないなら、認証ページに飛ばします
def render_login_user(request):
    """〇×ゲームの練習２"""
    if request.method == "POST":
        # `po_` は POST送信するパラメーター名の目印
        room_name = request.POST.get("po_room_name")
        my_piece = request.POST.get("po_my_piece")
        return redirect(f'/tic-tac-toe/v2/play/{room_name}/?&mypiece={my_piece}')
        #                               ^
        #               ------------------------------------------------------
        #               1
        # 1. http://example.com/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                       ----------------------------------------
    return render(request, "webapp1/tic-tac-toe/v2/match_request.html", {})
    #                                            ^
    #                       -----------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_request.html を取得
    #                            -----------------------------------------


def render_logout_user(request):
    """ログアウト"""
    logout(request)
    return redirect('ticTacToeV2_portal')
