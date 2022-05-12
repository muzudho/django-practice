from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


@login_required
def visitPortal1(request):
    """ポータル１"""
    template = loader.get_template('portal/portal1.html')
    #                               -------------------
    #                               1
    # 1. host1/webapp1/templates/portal/portal1.html を取得
    #                            -------------------

    context = {
        'dj_user': request.user,
        'dj_gamePath': 'tic-tac-toe2/',
        'dj_signUpPath': 'accounts/login/',
        'dj_logoutPath': 'accounts/logout/',
    }
    return HttpResponse(template.render(context, request))
