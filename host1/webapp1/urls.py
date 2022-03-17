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
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView #追加
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login-user', views.loginUser, name='loginUser'),
    path('admin/', admin.site.urls),

    # Allauth
    # https://sinyblog.com/django/django-allauth/
    path('', TemplateView.as_view(template_name='home.html'), name='home'), #追加。ログオン後のTOP画面の定義
    path('accounts/', include('allauth.urls')), #追加
    #

    path('practice1/page1.html', views.page1, name='page1'),

    # メンバー一覧
    path('members/', views.listMember, name='listMember'), # 追加
    #                                        ----------
    #                                        1
    # 1. HTMLテンプレートの中で {% url 'listMember' %} のような形でURLを取得するのに使える

    # メンバー読取
    path('members/read/<int:id>/', views.readMember, name='readMember'), # 追加
    #     ----------------------
    #     1
    # 1. `members/read/<数字列>/` というURLにマッチする。数字列は views.py の中で id という名前で取得できる

    # メンバー削除
    path('members/delete/<int:id>/', views.deleteMember, name='deleteMember'), # 追加
    #     ------------------------
    #     1
    # 1. `members/delete/<数字列>/` というURLにマッチする。数字列は views.py の中で id という名前で取得できる

    # メンバー作成
    path('members/create/', views.upsertMember, name='createMember'), # 追加

    # メンバー更新
    path('members/update/<int:id>/', views.upsertMember, name='updateMember'), # 追加
    #     ------------------------
    #     1
    # 1. `members/update/<数字列>/` というURLにマッチする。数字列は views.py の中で id という名前で取得できる

    # Vuetify練習
    path('vuetify2/hello1.html', views.readHello, name='readHello'), # 追加
    #     --------------------                          ----------
    #     1                                             2
    # 1. `vuetify2/hello1.html` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readHello' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify2/data-table1.html', views.readDataTable1, name='readDataTable1'), # 追加
    #     -------------------------                               --------------
    #     1                                                       2
    # 1. `vuetify2/data-table1.html` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readDataTable1' %} のような形でURLを取得するのに使える

    # Vuetify練習
    path('vuetify2/data-table2.html', views.readDataTable2, name='readDataTable2'), # 追加
    #     -------------------------                               --------------
    #     1                                                       2
    # 1. `vuetify2/data-table2.html` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readDataTable2' %} のような形でURLを取得するのに使える
]
