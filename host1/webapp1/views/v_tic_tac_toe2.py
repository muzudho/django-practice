from django.http import Http404
from django.shortcuts import render, redirect


#                   v
def indexOfTicTacToe2(request):
    """（追加） For Tic-tac-toe2"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe2/{room_name}/?&mypiece={myPiece}')
        #                             ^
    return render(request, "tic-tac-toe2/index.html", {})
    #                                  ^


#                      v
def playGameOfTicTacToe2(request, room_name):
    """（追加） For Tic-tac-toe2"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe2/game.html", context)
    #                                  ^
