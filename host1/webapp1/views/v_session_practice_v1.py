from django.shortcuts import render

from webapp1.models_helper.mh_session import get_all_logged_in_users
#    ------- ------------- ----------        -----------------------
#    1       2             3                 4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 関数名


def renderActiveUserList(request):
    """アクティブ ユーザー一覧"""

    context = {
        'users': get_all_logged_in_users()
    }
    return render(request, "session-practice/active-user-list.html", context)
    #                       --------------------------------------
    #                       1
    # 1. webapp1/templates/session-practice/active-user-list.html
    #                      --------------------------------------
