# See also: 📖[Custom Signup View in django-allauth](https://tech.serhatteker.com/post/2020-06/custom-signup-view-in-django-allauth/)
from allauth.account.views import LoginView, SignupView


class AccountsV1SignupView(SignupView):
    """django-allauth のサインアップ ビューをカスタマイズします
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/socialaccount/views.py)
    """

    # ファイルパス
    template_name = "allauth-customized/v1/account/signup.html"
    #                -----------------------------------------
    #                1
    # 1. host1/webapp1/templates/allauth-customized/v1/account/signup.html を取得
    #                            -----------------------------------------

    # You can also override some other methods of SignupView
    # Like below:
    # def form_valid(self, form):
    #     ...
    #
    # def get_context_data(self, **kwargs):
    #     ...


# グローバル変数
accounts_v1_signup_view = AccountsV1SignupView.as_view()


class AccountsV1LoginView(LoginView):
    """django-allauth のログイン ビューをカスタマイズします
    📖[views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)
    """

    # ファイルパス
    template_name = "allauth-customized/v1/account/login.html"
    #                ----------------------------------------
    #                1
    # 1. host1/webapp1/templates/allauth-customized/v1/account/login.html を取得
    #                            ----------------------------------------


# グローバル変数
accounts_v1_login_view = AccountsV1LoginView.as_view()
