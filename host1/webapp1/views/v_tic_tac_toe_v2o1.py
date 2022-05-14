from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


def visitPortal(request):
    """ポータル"""
    template = loader.get_template('tic-tac-toe/v2/portal.html')
    #                               --------------------------
    #                               1
    # 1. host1/webapp1/templates/tic-tac-toe/v2/portal.html を取得
    #                            --------------------------

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,
        'dj_matchRequestPath': 'tic-tac-toe/v2/match-request/',
        #                       -----------------------------
        #                       1
        # 1. http://example.com/tic-tac-toe/v2/match-request/
        #                       -----------------------------
        'dj_loginPath': 'tic-tac-toe/v2/login/',
        #                ---------------------
        #                1
        # 1. http://example.com/tic-tac-toe/v2/login/
        #                       ---------------------
        'dj_logoutPath': 'tic-tac-toe/v2/logout/',
        #                 ----------------------
        #                 1
        # 1. http://example.com/tic-tac-toe/v2/logout/
        #                       ----------------------
    }
    return HttpResponse(template.render(context, request))


@login_required  # 👈 このデコレーターを付けると、ログインしていないなら、認証ページに飛ばします
def loginUser(request):
    """〇×ゲームの練習２"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe/v2/play/{room_name}/?&mypiece={myPiece}')
        #                               ^
        #               ------------------------------------------------------
        #               1
        # 1. http://example.com/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                       ----------------------------------------
    return render(request, "tic-tac-toe/v2/match_request.html", {})
    #                                    ^
    #                       ---------------------------------
    #                       1
    # 1. host1/webapp1/templates/tic-tac-toe/v2/match_request.html を取得
    #                            ---------------------------------


def logoutUser(request):
    """ログアウト"""
    logout(request)
    return redirect('visitTicTacToeV2Portal')