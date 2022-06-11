# from django.contrib.auth.models import User # デバッグ用

import json
from webapp1.views import v_tic_tac_toe_v2
#                                        ^ two
#    ------- -----        ----------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

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

    _path_of_playing = "/tic-tac-toe/v3/playing/{0}/?&mypiece={1}"
    #                                 ^ three
    #                   -----------------------------------------
    #                   1
    # 1. http://example.com:8000/tic-tac-toe/v3/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                     ^ two
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        return v_tic_tac_toe_v2.match_application_render(request, MatchApplication._path_of_playing, MatchApplication._path_of_html, MatchApplication.on_sent, MatchApplication.open)
        #                     ^ two

    @staticmethod
    def on_sent(request):
        """送信後"""
        return match_application_on_sent(request)

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return v_tic_tac_toe_v2.match_application_open_context
        #                     ^ two


class Playing():
    """対局ページ"""

    _path_of_playing = "/tic-tac-toe/v2/playing/"
    #                                 ^ two
    #                   ------------------------
    #                   1
    # 1. http://example.com/tic-tac-toe/v2/playing/Elephant/
    #                      ------------------------

    _path_of_html = "webapp1/tic-tac-toe/v3/playing.html.txt"
    #                                     ^ three
    #                ---------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v3/playing.html.txt
    #                            ---------------------------------------

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        return v_tic_tac_toe_v2.playing_render(request, kw_room_name, Playing._path_of_playing, Playing._path_of_html, Playing.on_update)
        #                     ^ two

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass


# 以下、関数

def match_application_on_sent(request):
    """対局申込 - 送信後

    * ログインしていないユーザーが部屋に入っても 何も記録しません
    * ログインしているユーザーが部屋に入ってくると、以下のものを記録します（チェックイン）
    * Room.sente_id または Room.gote_id の空いている方に user.pk を上書き
    * user.profile.match_state を 3 （対局中）に上書き
    """

    # `po_` は POST送信するパラメーター名の目印
    # 部屋名
    po_room_name = request.POST.get("po_room_name")
    # 自分の駒。 X か O
    po_my_piece = request.POST.get("po_my_piece")

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

        # 自分の Profile レコード 取得
        profile = Profile.objects.get(user__pk=user_pk)
        #                             --------
        #                             1
        # 1. Profile テーブルと 1対1 で紐づいている親テーブル User の pk フィールド

        # print(f"[MatchApplication on_sent] profile={profile}")
        # print(
        #     f"[MatchApplication on_sent] profile.match_state={profile.match_state}")

        if po_my_piece == "X":
            # X を取った方は先手とします
            room.sente_id = user_pk
            # ユーザーの状態を対局中（3）にします
            profile.match_state = 3

        elif po_my_piece == "O":
            # O を取った方は後手とします
            #
            # * 先手と後手が同じユーザーでも構わないものとします
            room.gote_id = user_pk
            # ユーザーの状態を対局中（3）にします
            profile.match_state = 3

        else:
            # それ以外は観戦者として扱う
            # ユーザーの状態を観戦中（4）にします
            profile.match_state = 4

        # 先手と後手の両方が埋まったなら
        if not(room.sente_id is None or room.sente_id == 0 or room.gote_id is None or room.gote_id == 0):
            # 盤と棋譜を空っぽにする
            room.board = ""
            room.record = ""

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
