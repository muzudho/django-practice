import datetime
import json
from django.shortcuts import render

from webapp1.models_helper.mh_user import MhUser
#    ------- ------------- -------        ------
#    1       2             3              4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def render_user_list(request):
    """会員登録ユーザー一覧"""

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # Vue に渡すときは、 JSON オブジェクトではなく、 JSON 文字列です
        'dj_user_dic': json.dumps(MhUser.get_user_dic())
    }

    return render(request, "webapp1/practice/user-list.html", context)
    #                       -------------------------------
    #                       1
    # 1. webapp1/templates/webapp1/practice/user-list.html
    #                      -------------------------------


def render_user_list_v2(request):
    """会員登録ユーザー一覧 v2"""

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # Vue に渡すときは、 JSON オブジェクトではなく、 JSON 文字列です
        'dj_user_dic': json.dumps(MhUser.get_user_dic_v2()),
        #                                            ---
    }

    return render(request, "webapp1/practice/user-list-v2.html", context)
    #                       ----------------------------------
    #                       1
    # 1. webapp1/templates/webapp1/practice/user-list-v2.html
    #                      ----------------------------------


def render_waiting_for_match(request):
    """対局待合室"""

    context = {
    }

    return render(request, "webapp1/practice/waiting-for-match-v1.html", context)
    #                       ------------------------------------------
    #                       1
    # 1. webapp1/templates/webapp1/practice/waiting-for-match-v1.html
    #                      ------------------------------------------


def render_waiting_for_match_v2(request):
    """対局待合室"""

    # 現在日時
    dt_now = datetime.datetime.now()

    # 今何分？
    dt_minute = dt_now.minute

    # 5 で割り切れる分なら、リダイレクト
    if dt_minute % 5 == 0:
        redirect_path = "/tic-tac-toe/v2/"
    else:
        # リダイレクトしたくないときは空文字列を送る、と取り決めておきます
        redirect_path = ""

    context = {
        # FIXME 相対パス。 URL を urls.py で変更したいとき、反映されないがどうするか？
        "dj_redirect_path": redirect_path,
    }

    return render(request, "webapp1/practice/waiting-for-match-v2.html", context)
    #                       ------------------------------------------
    #                       1
    # 1. webapp1/templates/webapp1/practice/waiting-for-match-v2.html
    #                      ------------------------------------------
