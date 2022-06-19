"""webapp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from webapp1.views import v_accounts_v1
#    ------- -----        -------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # webapp1
    path('', include('webapp1.urls')),
    #    --           ------------
    #    1            2
    # 1. 例えば `http://example.com/` のような URLの直下
    # 2. `host1/webapp1/urls.py` の urlpatterns を (1.) にぶら下げます
    #           ------------

    # +----
    # | 認証

    # allauth の URLのパスのコピー
    path('accounts/v1/', include('allauth.urls')),
    #     ------------   -----------------------
    #     1
    # 1. 例えば `http://example.com/accounts/v1/` のような URLのパスの部分
    # 2. allauth の例えば `login/` のようなパスを 1. のパスにぶら下げる形で全てコピーします

    # サインアップ（会員登録）
    path("accounts/v1/signup/", view=v_accounts_v1.accounts_v1_signup_view,
         # ------------------        -------------------------------------
         # 1                        2
         name="accounts_v1_signup"),
    #          ------------------
    #          3
    # 1. 例えば `http://example.com/accounts/v1/signup/` のような URL のパスの部分
    #                              -------------------
    # 2. allauth の SignupView をカスタマイズしたオブジェクト
    # 3. HTMLテンプレートの中で {% url 'accounts_v1_signup' %} のような形でURLを取得するのに使える

    # ログイン
    path("accounts/v1/login/", view=v_accounts_v1.accounts_v1_login_view,
         # -----------------        ------------------------------------
         # 1                        2
         name="accounts_v1_login"),
    #          -----------------
    #          3
    # 1. 例えば `http://example.com/accounts/v1/login/` のような URL のパスの部分
    #                              -------------------
    # 2. v_accounts_v1.py ファイルの accounts_v1_login_view グローバル変数。ビューのオブジェクト
    # 3. HTMLテンプレートの中で {% url 'accounts_v1_login' %} のような形でURLを取得するのに使える

    # | 認証
    # +----
]
