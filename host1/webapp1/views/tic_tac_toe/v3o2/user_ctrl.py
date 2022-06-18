from webapp1.views.tic_tac_toe.v3o2.things import PC_EMPTY, PC_X_LABEL, PC_O_LABEL, PC_X, PC_O
#    ------- ---------------------- ------        --------...
#    1       2                      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 変数，クラス名等


class UserCtrl ():
    """ユーザーコントロール"""

    def __init__(self):
        """生成"""

        def doNothing():
            pass

        self._onDoMove = doNothing
        """イベントリスナー"""

    @property
    def onDoMove(self):
        return self._onDoMove

    @onDoMove.setter
    def onDoMove(self, value):
        """駒を置いたとき"""
        self._onDoMove = value

    def doMove(self, position, piece, sq):
        """駒を置きます

        Parameters
        ----------
        position : Position
            局面
        piece : str
            X か O
        sq : int
            升番号 0 <= sq

        Returns
        -------
        _type_
            駒を置けたら真、それ以外は偽
        """

        if position.getPieceBySq(sq) == PC_EMPTY:
            # 空升なら

            self._playeq.incrementCountOfMove()
            # 手数を１増やします

            # 駒を置きます
            if piece == PC_X_LABEL:
                self._playeq.setPiece(sq, PC_X)
            elif piece == PC_O_LABEL:
                self._playeq.setPiece(sq, PC_O)
            else:
                print(f"[Error] Invalid piece={piece}")
                return False

            print(f"[UserCtrl doMove] sq={sq} piece={piece}")
            self._onDoMove(sq, piece)

        return True
