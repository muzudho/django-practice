from django.http import Http404
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User # デバッグ用

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.models.m_user_profile import Profile
#    ------- ------ --------------        -------
#    1       2      3                     4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


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

        # Specification
        #
        # ログインしていないユーザーが部屋に入っても 何も記録しません
        #
        # ログインしているユーザーが部屋に入ってくると、以下のものを記録します（チェックイン）
        #
        # * Room.sente_id または Room.gote_id の空いている方に user.pk を上書き
        # * user.profile.match_state を 3 （対局中）に上書き

        # `po_` は POST送信するパラメーター名の目印
        # 部屋名
        po_room_name = request.POST.get("po_room_name")

        # 部屋の取得 または 新規作成
        #
        # * ID ではなく、部屋名から行う
        room_table_qs = Room.objects.filter(name=po_room_name)
        # print(
        #     f"[MatchApplication on_sent] po_room_name=[{po_room_name}] len={len(room_table_qs)}")

        if 1 <= len(room_table_qs):
            # （名前被りがあったなら）先頭の１つを取得
            room = room_table_qs[0]
            # print(f"[MatchApplication on_sent] first room=[{room}]")
            # print(
            #     f"[MatchApplication on_sent] first room .name=[{room.name}] .sente_id=[{room.sente_id}] .gote_id=[{room.gote_id}] .board=[{room.board}] .record=[{room.record}]")
        else:
            # 新規作成
            room = Room()
            room.name = po_room_name
            # print(f"[MatchApplication on_sent] new room=[{room}]")

        # print(f"[MatchApplication on_sent] request.user={request.user}")
        # print(
        #     f"[MatchApplication on_sent] request.user.is_authenticated={request.user.is_authenticated}")

        if request.user.is_authenticated:
            # ログインしたユーザーだった

            user_pk = request.user.pk
            # print(
            #     f"[MatchApplication on_sent] user_pk={user_pk} room.sente_id={room.sente_id} room.gote_id={room.gote_id}")

            # デバッグ
            # user = User.objects.get(pk=user_pk)
            # print(
            #     f"[MatchApplication on_sent] user username={user.username}")

            # sente_id フィールドに 自分のユーザーIdを上書き
            if room.sente_id is None or room.sente_id == 0:
                room.sente_id = user_pk
            elif room.gote_id is None or room.gote_id == 0:
                room.gote_id = user_pk

            # TODO 空いてなかったらどうする？

            # 自分の Profile レコード 取得
            profile = Profile.objects.get(user__pk=user_pk)
            #                             --------
            #                             1
            # 1. Profile テーブルと 1対1 で紐づいている親テーブル User の pk フィールド

            # print(f"[MatchApplication on_sent] profile={profile}")
            # print(
            #     f"[MatchApplication on_sent] profile.match_state={profile.match_state}")

            # ユーザーの状態を対局中（3）にします
            profile.match_state = 3

            # print(
            #     f"[MatchApplication on_sent] room .name=[{room.name}] .sente_id=[{room.sente_id}] .gote_id=[{room.gote_id}] .board=[{room.board}] .record=[{room.record}]")
            # TODO バリデーションチェック
            room.save()

            # print(
            #     f"[MatchApplication on_sent] prifile .match_state=[{profile.match_state}]")
            # TODO バリデーションチェック
            profile.save()

            # print(f"[MatchApplication on_sent] ★ 更新終わり")
        else:
            # ゲストだった
            # print(f"[MatchApplication on_sent] ★ ゲスト")
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
