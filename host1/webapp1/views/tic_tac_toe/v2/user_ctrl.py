from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class UserCtrl ():
    """ユーザーコントロール"""

    def __init__(self, playeq):
        """_summary_

        Parameters
        ----------
        playeq : _type_
            遊具
        """

        self._playeq = playeq
        """遊具"""

        def doNothing():
            pass

        self._onDoMove = doNothing
        """イベントリスナー"""

    @property
    def onDoMove(self):
        return self._onDoMove

    @onDoMove.setter
    def onDoMove(self, value):
        """石を置いたとき"""
        self._onDoMove = value

    def doMove(self, sq, piece):
        """石を置きます

        Parameters
        ----------
        sq : int
            升番号 0 <= sq
        piece : str
            X か O

        Returns
        -------
        _type_
            石を置けたら真、それ以外は偽
        """
        if self._playeq.gameoverState != game_rule.GAMEOVER_NONE:
            # Warning of illegal move
            print(
                f"Warning of illegal move. gameoverState={self._playeq.gameoverState}")

        if self._playeq.getPieceBySq(sq) == game_rule.PC_EMPTY:
            # 空升なら

            self._playeq.incrementCountOfMove()
            # 手数を１増やします

            # 石を置きます
            if piece == game_rule.PC_X_LABEL:
                self._playeq.setPiece(sq, game_rule.PC_X)
            elif piece == game_rule.PC_O_LABEL:
                self._playeq.setPiece(sq, game_rule.PC_O)
            else:
                print(f"[Error] Invalid piece={piece}")
                return False

            print(f"[UserCtrl doMove] sq={sq} piece={piece}")
            self._onDoMove(sq, piece)

        return True
