from webapp1.websocks.tic_tac_toe.v2.protocol import TicTacToeV2Protocol
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV3Protocol(TicTacToeV2Protocol):
    """サーバープロトコル"""

    def on_end(self, request):
        """対局終了時"""
        pass

    def on_move(self, request):
        """石を置いたとき"""

        sq = request.get("sq", None),
        my_piece = request.get("myPiece", None),

        # TODO room.board 文字列に石を追加したい
        # TODO room.record 文字列に座標を追加したい

        pass

    def on_start(self, request):
        """対局開始時"""
        pass
