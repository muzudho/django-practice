# See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
from allauth.account.views import SignupView, LoginView


class AccountV1SignupView(SignupView):
    """django-allauth のサインアップ ビューを継承します
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/views.py)
    """

    # ファイルパス
    template_name = "account/v1/signup.html"
    #                ------------------------
    #                1
    # 1. host1/webapp1/templates/account/v1/signup.html を取得
    #                            ----------------------

    # You can also override some other methods of SignupView
    # Like below:
    # def form_valid(self, form):
    #     ...
    #
    # def get_context_data(self, **kwargs):
    #     ...


# グローバル変数
account_v1_signup_view = AccountV1SignupView.as_view()


class AccountV1LoginView(LoginView):
    """django-allauth のログイン ビューを継承します
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)
    """

    # ファイルパス
    template_name = "account/v1/login.html"
    #                ------------------------
    #                1
    # 1. host1/webapp1/templates/account/v1/login.html を取得
    #                            ---------------------


# グローバル変数
account_v1_login_view = AccountV1LoginView.as_view()
