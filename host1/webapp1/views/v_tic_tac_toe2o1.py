from django.contrib.auth import logout
from django.shortcuts import redirect


def logoutUser(request):
    """ログアウト"""
    logout(request)
    return redirect('visitPortal1')
