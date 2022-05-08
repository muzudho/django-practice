from django.http import Http404
from django.shortcuts import render, redirect
from webapp1.models.m_tic_tac_toe3 import TicTacToeRoom3
#                                ^                     ^
#    ------- ------ --------------        --------------
#    1       2      3                     4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


#                   v
def indexOfTicTacToe3(request):
    """（追加） For Tic-tac-toe3"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe3/{room_name}/?&mypiece={myPiece}')
        #                             ^
    return render(request, "tic-tac-toe3/index.html", {})
    #                                  ^


#                      v
def playGameOfTicTacToe3(request, room_name):
    """（追加） For Tic-tac-toe3"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe3/game.html", context)
    #                                  ^
