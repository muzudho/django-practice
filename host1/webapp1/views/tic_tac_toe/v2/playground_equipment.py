from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class PlaygroundEquipment():
    """遊具"""

    def __init__(self):
        # あとで onStart(...) を呼出してください
        pass

    def onStart(self, myPiece):
        """対局開始時

        Parameters
        ----------
        myPiece : str
            "X", "O", "_"
        """

        self._board = [game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY,
                       game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY]
        """盤面"""

        self._countOfMove = 0
        """何手目"""

        self._isMyTurn = myPiece == game_rule.PC_X_LABEL
        """自分の手番か（初回は先手）"""

        self._isVisibleAlertWaitForOther = False
        """「相手の手番に着手しないでください」というアラートの可視性"""

        self._gameoverState = game_rule.GAMEOVER_NONE
        """ゲームオーバーしてません"""

        # イベントハンドラはそのまま

    def getPieceBySq(self, sq):
        """盤上のマス番号で示して、駒を取得

        Parameters
        ----------
        sq : int
            マス番号

        Returns
        -------
        _type_
            _description_
        """
        return self._board[sq]

    def setPiece(self, sq, piece):
        """盤上のマスに駒を上書きします

        Parameters
        ----------
        sq : int
            マス番号
        piece : str
            駒
        """
        self._board[sq] = piece

    def incrementCountOfMove(self):
        """手数を１増やします"""
        self._countOfMove += 1

    def isBoardFill(self):
        """マスがすべて埋まっていますか"""
        return self._countOfMove == 9

    def isThere3SamePieces(self):
        """同じ駒が３個ありますか"""
        return 5 <= self._countOfMove

    @property
    def isMyTurn(self):
        """私のターンですか"""
        return self._isMyTurn

    @isMyTurn.setter
    def isMyTurn(self, value):
        self._isMyTurn = value

    @property
    def isVisibleAlertWaitForOther(self):
        """「相手の手番に着手しないでください」というアラートの可視性"""
        return self._isVisibleAlertWaitForOther

    @isVisibleAlertWaitForOther.setter
    def isVisibleAlertWaitForOther(self, value):
        self._isVisibleAlertWaitForOther = value

    @property
    def gameoverState(self):
        """ゲームオーバー状態"""
        return self._gameoverState

    @gameoverState.setter
    def gameoverState(self, value):
        self._gameoverState = value
