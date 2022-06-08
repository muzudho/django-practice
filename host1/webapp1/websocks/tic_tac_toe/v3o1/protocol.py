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

    def on_end(self, request):
        """対局終了時"""
        pass

    def on_move(self, request):
        """石を置いたとき"""

        sq = request.get("sq", None),
        # my_piece = request.get("myPiece", None),
        print(
            f"[TicTacToeV3o1Protocol on_move] sq=[{sq}]")

        # `po_` は POST送信するパラメーター名の目印
        # 部屋名
        po_room_name = request.POST.get("po_room_name")
        # 自分の駒。 X か O
        po_my_piece = request.POST.get("po_my_piece")
        print(
            f"[TicTacToeV3o1Protocol on_move] po_room_name=[{po_room_name}] po_my_piece=[{po_my_piece}]")

        # 部屋の取得 または 新規作成
        #
        # * ID ではなく、部屋名から行う
        room_table_qs = Room.objects.filter(name=po_room_name)
        print(
            f"[TicTacToeV3o1Protocol on_move] len(room_table_qs)={len(room_table_qs)}")

        if 1 == len(room_table_qs):
            # FIXME 名前被りの部屋が存在すると正しく動きません
            room = room_table_qs[0]
        else:
            raise ValueError(f"room fail. po_room_name=[{po_room_name}]")

        # （デバッグ）現状を出力
        print(
            f"[TicTacToeV3o1Protocol on_move] now room.board=[{room.board}] room.record=[{room.record}]")

        # TODO room.board 文字列に石を追加したい
        # TODO room.record 文字列に座標を追加したい

        pass

    def on_start(self, request):
        """対局開始時"""
        pass
