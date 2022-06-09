from asgiref.sync import sync_to_async

from webapp1.websocks.tic_tac_toe.v2.protocol import TicTacToeV2Protocol
#                                  ^ two                       ^ two
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV3o1Protocol(TicTacToeV2Protocol):
    """サーバープロトコル"""

    def on_end(self, doc_received):
        """対局終了時"""
        pass

    async def on_move(self, doc_received, user):
        """石を置いたとき"""

        print(
            f"[TicTacToeV3o1Protocol on_move] doc_received={doc_received}")
        # [TicTacToeV3o1Protocol on_move] doc_received={'event': 'CtoS_Move', 'sq': 2, 'myPiece': 'X'}

        # ログインしていなければ AnonymousUser
        if user.is_anonymous:
            # ログインしていないユーザーの操作は記録しません
            return

        event = doc_received.get("event", None)
        # 石を置いたマス番号
        sq = doc_received.get("sq", None)
        # 自分の石
        my_piece = doc_received.get("myPiece", None)
        print(
            f"[TicTacToeV3o1Protocol on_move] user=[{user}] event=[{event}] sq=[{sq}] my_piece=[{my_piece}]")
        # [TicTacToeV3o1Protocol on_move] user=[muzudho] event=[CtoS_Move] sq=[2] my_piece=[X]

        # ユーザーに紐づく部屋を取得します
        # FIXME `sync_to_async` を用いて、一時的に非同期スレッドにする必要があります
        if my_piece == "X":
            room = await get_room_by_sente_id(user.pk)
        elif my_piece == "O":
            room = await get_room_by_gote_id(user.pk)
        else:
            raise ValueError(f"Unexpected my_piece = [{my_piece}]")

        print(
            f"[TicTacToeV3o1Protocol on_move] room=[{room}]")
        print(
            f"[TicTacToeV3o1Protocol on_move] room name=[{room.name}]")

        # （デバッグ）現状を出力
        print(
            f"[TicTacToeV3o1Protocol on_move] now room.board=[{room.board}] room.record=[{room.record}]")

        # 石を置きます
        #
        # * 盤が9マスになるように右を '.' で埋めます
        room.board = room.board.ljust(9, '.')
        print(
            f"[TicTacToeV3o1Protocol on_move] now2 room.board=[{room.board}]")

        room.board = f"{room.board[:sq]}{my_piece}{room.board[sq+1:]}"
        print(
            f"[TicTacToeV3o1Protocol on_move] now3 room.board=[{room.board}]")

        # 棋譜を書きます
        #
        # * 相手が AnonymousUser なら、相手の指し手が記録されていないものになります
        # * 9文字を超えるようなら、切り捨てます

        print(
            f"[TicTacToeV3o1Protocol on_move] now4 room.record=[{room.record}]")
        room.record = f"{room.record}{sq}"[:9]
        print(
            f"[TicTacToeV3o1Protocol on_move] now5 room.record=[{room.record}]")

        # 部屋を上書きします
        await save_room(room)

        print(
            f"[TicTacToeV3o1Protocol on_move] saved")

    def on_start(self, doc_received):
        """対局開始時"""
        pass


@sync_to_async
def get_room_by_sente_id(user_id):
    # FIXME １人のユーザーが複数の部屋にいる（多面指し）することは可能。部屋を一意に取得するには？
    return Room.objects.filter(sente_id=user_id)[0]


@sync_to_async
def get_room_by_gote_id(user_id):
    # FIXME １人のユーザーが複数の部屋にいる（多面指し）することは可能。部屋を一意に取得するには？
    return Room.objects.filter(sente_id=user_id)[0]


@sync_to_async
def save_room(room):
    room.save()
