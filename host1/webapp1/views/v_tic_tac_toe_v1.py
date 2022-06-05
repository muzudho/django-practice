from django.http import Http404
from django.shortcuts import render, redirect


class MatchApplication():
    """対局申込"""

    @staticmethod
    def render(request):
        """描画"""
        if request.method == "POST":
            # 送信後

            room_name = request.POST.get("room_name")
            myPiece = request.POST.get("my_piece")
            return redirect(f'/tic-tac-toe/v1/playing/{room_name}/?&mypiece={myPiece}')
            #                 -------------------------------------------------------
            #                 1
            # 1. http://example.com:8000/tic-tac-toe/v1/playing/Elephant/?&mypiece=X
            #                           --------------------------------------------

        # 訪問後
        return render(request, "webapp1/tic-tac-toe/v1/match_application.html", {})
        #                       ---------------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v1/match_application.html
        #                            ---------------------------------------------


class Playing():
    """対局画面"""

    @staticmethod
    def render(request, room_name):
        """描画"""

        myPiece = request.GET.get("mypiece")
        if myPiece not in ['X', 'O']:
            raise Http404(f"My piece '{myPiece}' does not exists")
        context = {
            "my_piece": myPiece,
            "room_name": room_name
        }
        return render(request, "webapp1/tic-tac-toe/v1/playing.html", context)
        #                       -----------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v1/playing.html
        #                            -----------------------------------
