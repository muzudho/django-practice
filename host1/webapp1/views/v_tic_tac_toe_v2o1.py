"""〇×ゲームの練習２"""
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
            'dj_pathOfMatchApplication': '/tic-tac-toe/v2/match-application/',
            #                             ---------------------------------
            #                             1
            # 1. http://example.com/tic-tac-toe/v2/match-application/
            #                      ----------------------------------
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


class LoggingIn():
    """ログイン中"""

    _path_of_playing = "/tic-tac-toe/v2/playing/{0}/?&mypiece={1}"
    #                                 ^ two
    #                   -----------------------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    _path_of_match_application = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                                  ^ two
    #                             ---------------------------------------------
    #                             1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @classmethod
    @property
    def path_of_playing(clazz):
        return clazz._path_of_playing

    @classmethod
    @property
    def path_of_match_application(clazz):
        return clazz._path_of_match_application

    @login_required  # 👈 このデコレーターを付けると、ログインしていないなら、 settings.py の LOGIN_URL で指定した URL に飛ばします
    @classmethod
    def render(clazz, request):
        """描画"""

        if request.method == "POST":
            # 送信後

            # `po_` は POST送信するパラメーター名の目印
            room_name = request.POST.get("po_room_name")
            my_piece = request.POST.get("po_my_piece")

            return redirect(clazz.path_of_playing.format(room_name, my_piece))

        # 訪問後
        return render(request, clazz.path_of_match_application, {})


class LoggingOut():
    """ログアウト中"""

    @staticmethod
    def render(request):
        """描画"""

        logout(request)  # Django の認証機能のログアウトを使う

        return redirect('ticTacToeV2_portal')  # ホームに戻る
