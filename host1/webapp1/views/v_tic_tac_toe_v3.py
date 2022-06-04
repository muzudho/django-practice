from django.http import Http404
from django.shortcuts import render, redirect


def render_match_request(request):
    """対局要求"""
    if request.method == "POST":
        # `po_` は POST送信するパラメーター名の目印
        room_name = request.POST.get("po_room_name")
        my_piece = request.POST.get("po_my_piece")
        return redirect(f'/tic-tac-toe/v3/play/{room_name}/?&mypiece={my_piece}')
        #                               ^ three
        #                 ----------------------------------------------------
        #                 1
        # 1. http://example.com:8000/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                           -----------------------------------------
    return render(request, "webapp1/tic-tac-toe/v2/match_request.html", {})
    #                                            ^ two
    #                       -----------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_request.html
    #                            -----------------------------------------


def render_play(request, kw_room_name):
    """対局画面"""
    my_piece = request.GET.get("mypiece")
    if my_piece not in ['X', 'O']:
        raise Http404(f"My piece '{my_piece}' does not exists")

    # `dj_` は Djangoでレンダーするパラメーター名の目印
    context = {
        "dj_room_name": kw_room_name,
        "dj_my_piece": my_piece,
    }
    return render(request, "webapp1/tic-tac-toe/v3/play.html.txt", context)
    #                                            ^ three
    #                       ------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/play.html.txt
    #                            ------------------------------------
