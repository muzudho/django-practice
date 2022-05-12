from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required  # 👈 このデコレーターを付けると、ログインしていないなら、認証ページに飛ばします
def loginUser(request):
    """〇×ゲームの練習２"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe2/{room_name}/?&mypiece={myPiece}')
        #                             ^
    return render(request, "tic-tac-toe2/index.html", {})
    #                                  ^


def logoutUser(request):
    """ログアウト"""
    logout(request)
    return redirect('visitPortal1')
