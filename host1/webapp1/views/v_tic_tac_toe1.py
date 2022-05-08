from django.http import Http404
from django.shortcuts import render, redirect

def indexOfTicTacToe1(request):
    """（追加） For Tic-tac-toe"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe1/{room_name}/?&mypiece={myPiece}')
    return render(request, "tic-tac-toe1/index.html", {})


def playGameOfTicTacToe1(request, room_name):
    """（追加） For Tic-tac-toe"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe1/game.html", context)
