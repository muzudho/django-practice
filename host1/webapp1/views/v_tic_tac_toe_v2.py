from django.http import Http404
from django.shortcuts import render, redirect


class MatchApplication():
    """対局申込"""

    path_of_playing = "/tic-tac-toe/v2/playing/{0}/?&mypiece={1}"
    #                                ^ two
    #                  -----------------------------------------
    #                  1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    path_of_match_application = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                                 ^ two
    #                            ---------------------------------------------
    #                            1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        if request.method == "POST":
            # 送信後

            # `po_` は POST送信するパラメーター名の目印
            room_name = request.POST.get("po_room_name")
            my_piece = request.POST.get("po_my_piece")

            return redirect(MatchApplication.path_of_playing.format(room_name, my_piece))

        # 訪問後
        return render(request, MatchApplication.path_of_match_application, {})


class Playing():

    path_of_playing = "/tic-tac-toe/v2/playing/"
    #                                ^ two

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
            "dj_path_of_playing": Playing.path_of_playing,
        }
        return render(request, "webapp1/tic-tac-toe/v2/playing.html.txt", context)
        #                                            ^
        #                       ---------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/playing.html.txt
        #                            ---------------------------------------
