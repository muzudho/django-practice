from django.http import HttpResponse
from django.template import loader


def render_home(request):
    """ホーム"""
    template = loader.get_template('webapp1/home/v1/home.html')
    #                               -------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/home/v1/home.html を取得
    #                            -------------------------

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,

        'dj_lobbyPath': '/lobby/v1/',
        #                ----------
        #                1
        # 1. http://example.com/lobby/v1/
        #                      ----------

        'dj_ticTacToePath': '/tic-tac-toe/v2/match-application/',
        #                    ----------------------------------
        #                    1
        # 1. http://example.com/tic-tac-toe/v2/match-application/
        #                      ----------------------------------

        'dj_loginPath': '/accounts/v1/login/',
        #                -------------------
        #                1
        # 1. http://example.com/accounts/v1/login/
        #                      -------------------

        'dj_logoutPath': '/accounts/v1/logout/',
        #                 --------------------
        #                 1
        # 1. http://example.com/accounts/v1/logout/
        #                      --------------------
    }

    return HttpResponse(template.render(context, request))
