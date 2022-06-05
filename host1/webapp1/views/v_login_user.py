from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import redirect


class LoggingIn():
    """ログイン中"""

    @login_required  # 👈 このデコレーターを付けると、ログインしていないなら、 settings.py の LOGIN_URL で指定した URL に飛ばします
    @staticmethod
    def render(request):
        """描画"""

        template = loader.get_template('webapp1/practice/login-user.html')
        #                               --------------------------------
        #                               1
        # 1. host1/webapp1/templates/webapp1/practice/login-user.html を取得
        #                            --------------------------------
        #    webapp1 が２回出てくるのはテクニックのようです

        user = request.user
        context = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return HttpResponse(template.render(context, request))


class LoggingOut():
    """ログアウト中"""

    @staticmethod
    def render(request):
        """描画"""

        logout(request)  # Django の認証機能のログアウトを使う

        return redirect('home')  # ホームに戻る
