import json
from django.shortcuts import render

from webapp1.models_helper.mh_users import get_user_dic
#    ------- ------------- --------        ------
#    1       2             3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def render_user_list(request):
    """会員登録ユーザー一覧"""

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # Vue に渡すときは、 JSON オブジェクトではなく、 JSON 文字列です
        'dj_user_dic': json.dumps(get_user_dic())
    }

    return render(request, "webapp1/practice/user-list.html", context)
    #                       -------------------------------
    #                       1
    # 1. webapp1/templates/webapp1/practice/user-list.html
    #                      -------------------------------


def render_waiting_for_match(request):
    """対局待合室"""

    context = {
    }

    return render(request, "webapp1/practice/waiting-for-match-v1.html", context)
    #                       ------------------------------------------
    #                       1
    # 1. webapp1/templates/webapp1/practice/waiting-for-match-v1.html
    #                      ------------------------------------------
