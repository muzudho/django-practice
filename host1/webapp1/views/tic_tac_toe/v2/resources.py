import json
from django.http import Http404
from django.shortcuts import render, redirect


# 以下、よく使う定型データ


# 対局申込 - 訪問後
match_application_open_context = {
    # `dj_` は Djangoでレンダーするパラメーター名の目印
    # 入場者データ
    "dj_visitor_value": "X",
    # Python と JavaScript 間で配列データを渡すために JSON 文字列形式にします
    "dj_visitor_choices": json.dumps(["X", "O"]),
}


# 以下、ロジック


class MatchApplication():
    """対局申込"""

    _path_of_playing = "/tic-tac-toe/v2/playing/{0}/?&mypiece={1}"
    #                                 ^ two
    #                   -----------------------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                     ^ two
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        return render_match_application(request, MatchApplication._path_of_playing, MatchApplication._path_of_html, MatchApplication.on_sent, MatchApplication.open)

    @staticmethod
    def on_sent(request):
        """送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return match_application_open_context


class Playing():
    """対局中"""

    _path_of_playing = "/tic-tac-toe/v2/playing/"
    #                                 ^ two
    #                   ------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/
    #                           ------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/playing.html.txt"
    #                                     ^ two
    #                ---------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/playing.html.txt
    #                            ---------------------------------------

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        return render_playing(request, kw_room_name, Playing._path_of_playing, Playing._path_of_html, Playing.on_update)

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass


# 以下、関数


def render_match_application(request, path_of_playing, path_of_html, on_sent, open):
    """対局申込 - 描画"""
    if request.method == "POST":
        # 送信後
        on_sent(request)

        # `po_` は POST送信するパラメーター名の目印
        po_room_name = request.POST.get("po_room_name")
        po_my_piece = request.POST.get("po_my_piece")

        # TODO バリデーションチェックしたい

        return redirect(path_of_playing.format(po_room_name, po_my_piece))

    # 訪問後
    context = open(request)

    return render(request, path_of_html, context)


def render_playing(request, kw_room_name, path_of_playing, path_of_html, on_update):
    """対局中 - 描画"""
    my_piece = request.GET.get("mypiece")
    if my_piece not in ['X', 'O']:
        raise Http404(f"My piece '{my_piece}' does not exists")

    on_update(request)

    # `dj_` は Djangoでレンダーするパラメーター名の目印
    context = {
        "dj_room_name": kw_room_name,
        "dj_my_piece": my_piece,
        "dj_path_of_playing": path_of_playing,
    }
    return render(request, path_of_html, context)
