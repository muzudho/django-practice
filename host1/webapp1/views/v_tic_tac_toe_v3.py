from django.http import Http404
from django.shortcuts import render, redirect


class MatchApplication():
    """対局申込ページ"""

    @staticmethod
    def render(request):
        """描画"""

        if request.method == "POST":
            # 送信後
            MatchApplication.on_sent(request)

            # `po_` は POST送信するパラメーター名の目印
            room_name = request.POST.get("po_room_name")
            my_piece = request.POST.get("po_my_piece")
            return redirect(f'/tic-tac-toe/v3/playing/{room_name}/?&mypiece={my_piece}')
            #                               ^ three
            #                 --------------------------------------------------------
            #                 1
            # 1. http://example.com:8000/tic-tac-toe/v3/playing/Elephant/?&mypiece=X
            #                           --------------------------------------------

        # 訪問後
        MatchApplication.on_visited(request)
        return render(request, "webapp1/tic-tac-toe/v2/match_application.html", {})
        #                                            ^ two
        #                       ---------------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
        #                            ---------------------------------------------

    @staticmethod
    def on_sent(request):
        """送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass

    @staticmethod
    def on_visited(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く
        pass


class Playing():
    """対局ページ"""

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        my_piece = request.GET.get("mypiece")
        if my_piece not in ['X', 'O']:
            raise Http404(f"My piece '{my_piece}' does not exists")

        Playing.on_update(request)

        # `dj_` は Djangoでレンダーするパラメーター名の目印
        context = {
            "dj_room_name": kw_room_name,
            "dj_my_piece": my_piece,
        }
        return render(request, "webapp1/tic-tac-toe/v3/playing.html.txt", context)
        #                                            ^ three
        #                       ---------------------------------------
        #                       1
        # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/playing.html.txt
        #                            ---------------------------------------

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass
