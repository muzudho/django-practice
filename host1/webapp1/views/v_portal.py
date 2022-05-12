from django.http import HttpResponse
from django.template import loader


def visitPortal1(request):
    """ポータル１"""
    template = loader.get_template('portal/portal1.html')
    context = {
        'dj_gamePath': 'tic-tac-toe2/',
        'dj_signUpPath': 'accounts/login/',
    }
    return HttpResponse(template.render(context, request))
