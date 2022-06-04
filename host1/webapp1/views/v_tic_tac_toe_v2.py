from django.http import Http404
from django.shortcuts import render, redirect


def render_match_request(request):
    """対局要求"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe/v2/play/{room_name}/?&mypiece={myPiece}')
        #                               ^
        #                 ----------------------------------------------------
        #                 1
        # 1. http://example.com:8000/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                           -----------------------------------------
    return render(request, "webapp1/tic-tac-toe/v2/match_request.html", {})
    #                                            ^
    #                       -----------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_request.html
    #                            -----------------------------------------


def render_play(request, room_name):
    """対局画面"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "webapp1/tic-tac-toe/v2/play.html.txt", context)
    #                                            ^
    #                       ------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/play.html.txt
    #                            ------------------------------------
