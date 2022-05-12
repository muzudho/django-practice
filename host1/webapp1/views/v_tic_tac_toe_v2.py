from django.http import Http404
from django.shortcuts import render, redirect


def visitEntry(request):
    """エントリー画面"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe/v2/play/{room_name}/?&mypiece={myPiece}')
        #                               ^
        #                 ----------------------------------------------------
        #                 1
        # 1. http://example.com:8000/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                           -----------------------------------------
    return render(request, "tic-tac-toe/v2/entry.html", {})
    #                                    ^
    #                       -------------------------
    #                       1
    # 1. webapp1/templates/tic-tac-toe/v2/entry.html
    #                      -------------------------


def visitPlay(request, room_name):
    """対局画面"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe/v2/play.html", context)
    #                                    ^
    # 1. webapp1/templates/tic-tac-toe/v2/play.html
    #                      ------------------------
