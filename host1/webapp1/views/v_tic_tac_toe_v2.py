from django.http import Http404
from django.shortcuts import render, redirect


class MatchApplication():
    """対局申込"""

    @staticmethod
    def render(request):
        """描画"""
        if request.method == "POST":
            # 送信後

            # `po_` は POST送信するパラメーター名の目印
            room_name = request.POST.get("po_room_name")
            my_piece = request.POST.get("po_my_piece")
            return redirect(f'/tic-tac-toe/v2/playing/{room_name}/?&mypiece={my_piece}')
            #                               ^
            #                 --------------------------------------------------------
            #                 1
            # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&mypiece=X
            #                           --------------------------------------------

        # 訪問後
        return render(request, "webapp1/tic-tac-toe/v2/match_application.html", {})
        #                                            ^
        #                       ---------------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
        #                            ---------------------------------------------


class Playing():

    @staticmethod
    def render(request, kw_room_name):
        """対局画面"""

        my_piece = request.GET.get("mypiece")
        if my_piece not in ['X', 'O']:
            raise Http404(f"My piece '{my_piece}' does not exists")

        # `dj_` は Djangoでレンダーするパラメーター名の目印
        context = {
            "dj_room_name": kw_room_name,
            "dj_my_piece": my_piece,
        }
        return render(request, "webapp1/tic-tac-toe/v2/playing.html.txt", context)
        #                                            ^
        #                       ---------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/playing.html.txt
        #                            ---------------------------------------
