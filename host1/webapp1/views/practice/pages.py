import datetime
from django.shortcuts import render


def render_waiting_for_match(request):
    """対局待合室"""

    context = {
    }

    return render(request, "webapp1/practice/waiting-for-match-v1.html", context)
    #                       ------------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/practice/waiting-for-match-v1.html
    #                            ------------------------------------------


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
    # 1. host1/webapp1/templates/webapp1/practice/waiting-for-match-v2.html
    #                            ------------------------------------------
