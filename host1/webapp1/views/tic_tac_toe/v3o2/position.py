from webapp1.views.tic_tac_toe.v3o2.things import Board, Record
#    ------- ---------------------- ------        -------------
#    1       2                      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.views.tic_tac_toe.v3o2.concepts import MyTurn
#    ------- ---------------------- --------        ------
#    1       2                      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class Position():
    """局面"""

    def __init__(self, myPiece):
        """初期化

        * 対局開始時

        Parameters
        ----------
        myPiece : str
            "X", "O", "_"
        """
        print(f"[Position constructor] myPiece=${myPiece}")

        self._board = Board()
        """盤面"""

        self._record = Record()
        """棋譜"""

        self._myTurn = MyTurn(myPiece)
        """自分の手番"""

    @property
    def board(self):
        """盤"""
        return self._board

    @property
    def record(self):
        """棋譜"""
        return self._record

    @property
    def myTurn(self):
        """自分のターン"""
        return self._myTurn

    @property
    def isBoardFill(self):
        """マスがすべて埋まっていますか"""
        return self.record.length == 9

    @property
    def isThere3SamePieces(self):
        """同じ駒が３個ありますか"""
        return 5 <= self.record.length

    def dump(self, indent):
        """ダンプ"""
        return f"""
{indent}Position
{indent}--------
{indent}{self._board.dump(indent + "    ")}
{indent}{self._record.dump(indent + "    ")}
{indent}{self._myTurn.dump(indent + "    ")}"""
