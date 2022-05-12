from django.shortcuts import render, redirect


def redirectOldTicTacToe2(request):
    """URLが変わった

    Old
    http://example.com/tic-tac-toe2

    New
    http://example.com/portal/tic-tac-toe2
    """
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/portal/tic-tac-toe2/{room_name}/?&mypiece={myPiece}')
    #                     ----------------------------------------------------
    #                     1
    # 1. http://example.com/portal/tic-tac-toe2/Elephant/?&mypiece=X
    #                      -----------------------------------------

    return render(request, "tic-tac-toe2/index.html", {})
    #                       -----------------------
    #                       1
    # 1. webapp1/templates/tic-tac-toe2/index.html
    #                      -----------------------
