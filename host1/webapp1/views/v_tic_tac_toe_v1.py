from django.http import Http404
from django.shortcuts import render, redirect


class MatchApplication():
    """対局申込"""

    _path_of_playing = "/tic-tac-toe/v1/playing/{0}/?&mypiece={1}"
    #                   -----------------------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v1/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v1/match_application.html"
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v1/match_application.html
    #                            ---------------------------------------------

    def render(request):
        """描画"""
        return match_application_render(request, MatchApplication._path_of_playing, MatchApplication._path_of_html)


class Playing():
    """対局画面"""

    _path_of_html = "webapp1/tic-tac-toe/v1/playing.html"
    #                -----------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v1/playing.html
    #                            -----------------------------------

    def render(request, room_name):
        """描画"""
        return playing_render(request, room_name, Playing._path_of_html)


# 以下、関数


def match_application_render(request, path_of_playing, path_of_html):
    """対局申込 - 描画"""
    if request.method == "POST":
        # 送信後
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        # TODO バリデーションチェックしたい
        return redirect(path_of_playing.format(room_name, myPiece))

    # 訪問後
    return render(request, path_of_html, {})


def playing_render(request, room_name, path_of_html):
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, path_of_html, context)
