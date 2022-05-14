from django.http import HttpResponse
from django.template import loader


def visitHome(request):
    """ホーム"""
    template = loader.get_template('home/v2/home.html')
    #                               -----------------
    #                               1
    # 1. host1/webapp1/templates/home/v2/home.html を取得
    #                            -----------------

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,
        'dj_ticTacToePath': 'tic-tac-toe/v2/',
        #                    ---------------
        #                    1
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
