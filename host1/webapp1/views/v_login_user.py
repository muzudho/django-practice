from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import redirect


@login_required
def loginUser(request):

    template = loader.get_template('webapp1/login-user.html')
    #                               -----------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/login-user.html を取得
    #                            -----------------------
    #    webapp1 が２回出てくるのはテクニックのようです

    user = request.user
    context = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return HttpResponse(template.render(context, request))


def logoutUser(request):
    """ログアウト"""
    logout(request)
    return redirect('home')
