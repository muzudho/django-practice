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
    path('members/', views.memberList, name='memberList'), # 追加
    # メンバー読取
    path('members/read', views.memberRead, name='memberRead'), # 追加
]
