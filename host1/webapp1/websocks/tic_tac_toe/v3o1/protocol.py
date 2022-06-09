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

    def on_move(self, doc_received, user):
        """石を置いたとき"""

        # ログインしていなければ AnonymousUser
        if user.is_anonymous:
            # ログインしていないユーザーの操作は記録しません
            return

        print(
            f"[TicTacToeV3o1Protocol on_move] doc_received={doc_received}")
        # [TicTacToeV3o1Protocol on_move] doc_received={'event': 'CtoS_Move', 'sq': 2, 'myPiece': 'X'}

        event = doc_received.get("event", None),
        # 石を置いたマス番号
        sq = doc_received.get("sq", None),
        # 自分の石
        my_piece = doc_received.get("myPiece", None),
        print(
            f"[TicTacToeV3o1Protocol on_move] user=[{user}] event=[{event}] sq=[{sq}] my_piece=[{my_piece}]")

        # ユーザーに紐づく部屋を取得します
        if my_piece == "X":
            room = Room.objects.get(sente_id=user.pk)
        elif my_piece == "O":
            room = Room.objects.get(gote_id=user.pk)
        else:
            raise ValueError(f"Unexpected my_piece = [{my_piece}]")

        print(
            f"[TicTacToeV3o1Protocol on_move] room name=[{room.name}]")

        # （デバッグ）現状を出力
        print(
            f"[TicTacToeV3o1Protocol on_move] now room.board=[{room.board}] room.record=[{room.record}]")

        # 石を置きます
        #
        # * 盤が9マスになるように右を '.' で埋めます
        room.board.ljust(9, '.')
        room.board[sq] = my_piece

        # 棋譜を書きます
        #
        # * 相手が AnonymousUser なら、相手の指し手が記録されていないものになります
        # * 空文字列か、そうでなければ 末尾はカンマで終わります
        room.record = f"{room.record}{sq},"

        # 部屋を上書きします
        room.save()

    def on_start(self, doc_received):
        """対局開始時"""
        pass
