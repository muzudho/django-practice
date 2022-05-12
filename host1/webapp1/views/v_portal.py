from django.http import HttpResponse
from django.template import loader


def visitPortal1(request):
    """ポータル１"""
    template = loader.get_template('portal/portal1.html')
    #                               -------------------
    #                               1
    # 1. host1/webapp1/templates/portal/portal1.html を取得
    #                            -------------------

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_user': request.user,
        'dj_gamePath': 'tic-tac-toe2/',
        #               -------------
        #               1
        # 1. http://example.com/tic-tac-toe2/
        #                       -------------
        'dj_signUpPath': 'accounts/login/',
        #                 ---------------
        #                 1
        # 1. http://example.com/accounts/login/
        #                       ---------------
        'dj_logoutPath': 'logout/tic-tac-toe2',
        #                 -------------------
        #                 1
        # 1. http://example.com/logout/tic-tac-toe2
        #                       -------------------
    }
    return HttpResponse(template.render(context, request))
