from django.http import Http404
from django.shortcuts import render, redirect


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
        return match_application_render(request, MatchApplication._path_of_playing, MatchApplication._path_of_html)


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
        return playing_render(request, kw_room_name, Playing._path_of_playing, Playing._path_of_html)


# 以下、関数


def match_application_render(request, path_of_playing, path_of_match_application):
    """対局申込 - 描画"""
    if request.method == "POST":
        # 送信後

        # `po_` は POST送信するパラメーター名の目印
        room_name = request.POST.get("po_room_name")
        my_piece = request.POST.get("po_my_piece")

        return redirect(path_of_playing.format(room_name, my_piece))

    # 訪問後
    return render(request, path_of_match_application, {})


def playing_render(request, kw_room_name, path_of_playing, path_of_html):
    """対局中 - 描画"""
    my_piece = request.GET.get("mypiece")
    if my_piece not in ['X', 'O']:
        raise Http404(f"My piece '{my_piece}' does not exists")

    # `dj_` は Djangoでレンダーするパラメーター名の目印
    context = {
        "dj_room_name": kw_room_name,
        "dj_my_piece": my_piece,
        "dj_path_of_playing": path_of_playing,
    }
    return render(request, path_of_html, context)
