from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import redirect


class LoggingIn():
    """ログイン中"""

    @login_required  # 👈 このデコレーターを付けると、ログインしていないなら、認証ページに飛ばします
    @staticmethod
    def render(request):
        """描画"""

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


def render_logout_user(request):
    """ログアウト"""
    logout(request)
    return redirect('home')
