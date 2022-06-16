from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class JudgeCtrl():
    """審判コントロール"""

    def __init__(self, playeq, userCtrl):
        """生成

        Parameters
        ----------
        playeq:
            遊具
        userCtrl:
            ユーザーコントロール
        """

        self._playeq = playeq
        """遊具"""

        self._userCtrl = userCtrl
        """ユーザーコントロール"""

        def doNothing():
            pass

        self._onWon = doNothing
        """イベントリスナー"""

        self._onDraw = doNothing

    def onWon(self, func):
        """勝ったとき"""
        self._onWon = func

    def onDraw(self, func):
        """引き分けたとき"""
        self._onDraw = func

    def doJudge(self, myPiece):
        """ゲームオーバー判定"""

        self._playeq.gameoverState = self.makeGameoverState()
        print(f"[doJudge] gameoverState={self._playeq.gameoverState}")

        if self._playeq.gameoverState == game_rule.GAMEOVER_WIN:
            self._onWon(myPiece)
        elif self._playeq.gameoverState == game_rule.GAMEOVER_DRAW:
            self._onDraw()
        elif self._playeq.gameoverState == game_rule.GAMEOVER_LOSE:
            pass
        elif self._playeq.gameoverState == game_rule.GAMEOVER_NONE:
            pass
        else:
            raise ValueError(
                f"Unexpected gameoverState={self._playeq.gameoverState}")

    def makeGameoverState(self):
        """ゲームオーバー判定

        * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください

        Returns
        -------
        ゲームオーバー状態
        """
        print(
            f"[makeGameoverState] isThere3SamePieces={self._playeq.isThere3SamePieces()}")
        if self._playeq.isThere3SamePieces():
            for squaresOfWinPattern in game_rule.WIN_PATTERN:
                print(
                    f"[makeGameoverState] self.isPieceInLine(squaresOfWinPattern)={self.isPieceInLine(squaresOfWinPattern)}")
                if self.isPieceInLine(squaresOfWinPattern):
                    print(
                        f"[makeGameoverState] self._playeq.isMyTurn={self._playeq.isMyTurn}")
                    if self._playeq.isMyTurn:
                        # 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return game_rule.GAMEOVER_LOSE
                    else:
                        # 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return game_rule.GAMEOVER_WIN

        if self._playeq.isBoardFill():
            # 勝ち負けが付かず、盤が埋まったら引き分け
            return game_rule.GAMEOVER_DRAW

        # ゲームオーバーしてません
        return game_rule.GAMEOVER_NONE

    def isPieceInLine(self, squaresOfWinPattern):
        """石が３つ並んでいるか？

        Parameters
        ----------
        squaresOfWinPattern : _type_
            勝ちパターン

        Returns
        -------
        _type_
            並んでいれば真、それ以外は偽
        """
        return self._playeq.getPieceBySq(squaresOfWinPattern[0]) != game_rule.PC_EMPTY and \
            self._playeq.getPieceBySq(squaresOfWinPattern[0]) == self._playeq.getPieceBySq(squaresOfWinPattern[1]) \
            and self._playeq.getPieceBySq(squaresOfWinPattern[0]) == self._playeq.getPieceBySq(squaresOfWinPattern[2])
