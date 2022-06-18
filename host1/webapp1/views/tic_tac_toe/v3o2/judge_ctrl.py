from webapp1.views.tic_tac_toe.v3o2.things import PC_EMPTY
#    ------- ---------------------- ------        --------
#    1       2                      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 変数，クラス名等

from webapp1.views.tic_tac_toe.v3o2.concepts import WIN_PATTERN, GameoverSet
#    ------- ---------------------- --------        -----------...
#    1       2                      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 変数，クラス名等


class JudgeCtrl():
    """審判コントロール"""

    def __init__(self):
        """生成"""

        def ignore(piece_moved, gameover_set_value):
            pass

        self._onJudged = ignore
        """判断したとき"""

    @property
    def onJudged(self, value):
        """判断したとき"""
        self._onJudged = value

    def doJudge(self, position, piece_moved):
        """ゲームオーバー判定

        * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください

        Parameters
        ----------
        position : Position
            局面"""

        gameover_set_value = self.makeGameoverState(position)
        print(f"[doJudge] gameover_set_value={gameover_set_value}")
        self._onJudged(piece_moved, gameover_set_value)

    def makeGameoverState(self, position):
        """ゲームオーバー判定

        * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください

        Returns
        -------
        ゲームオーバー状態
        """
        if self._playeq.isThere3SamePieces():
            for squaresOfWinPattern in WIN_PATTERN:
                if self.isPieceInLine(position, squaresOfWinPattern):
                    if position.myTurn.isTrue:
                        # 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return GameoverSet.lose
                    else:
                        # 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return GameoverSet.win

        if position.isBoardFill:
            # 勝ち負けが付かず、盤が埋まったら引き分け
            return GameoverSet.draw

        # ゲームオーバーしてません
        return GameoverSet.none

    def isPieceInLine(self, position, squaresOfWinPattern):
        """駒が３つ並んでいるか？

        Parameters
        ----------
        position : Position
            局面
        squaresOfWinPattern : _type_
            勝ちパターン

        Returns
        -------
        _type_
            並んでいれば真、それ以外は偽
        """
        return position.board.getPieceBySq(squaresOfWinPattern[0]) != PC_EMPTY and \
            position.board.getPieceBySq(squaresOfWinPattern[0]) == position.board.getPieceBySq(squaresOfWinPattern[1]) and \
            position.board.getPieceBySq(
                squaresOfWinPattern[0]) == position.board.getPieceBySq(squaresOfWinPattern[2])
