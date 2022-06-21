from webapp1.views.tic_tac_toe.v3o2 import things
#    ------- ----------------------        ------
#    1       2                             3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class RoomState ():
    """部屋の状態"""

    @staticmethod
    @property
    def none():
        """ゲームしてません"""
        return 0

    @staticmethod
    @property
    def playing():
        """ゲーム中"""
        return 1

    def __init__(self, value, onChangeValue):
        """生成

        Parameters
        ----------
        value : int
            _description_
        onChangeValue : function
            値の変更時
        """
        print(f"[RoomState constructor]")

        self._value = value
        self._onChangeValue = onChangeValue

    @property
    def value(self):
        """値"""
        return self._value

    @value.setter
    def value(self, value):
        print(f"[RoomState set value]")

        if self._value == value:
            return

        oldValue = self._value
        self._value = value
        self._onChangeValue(oldValue, self._value)

    def dump(self, indent):
        """ダンプ

        Parameters
        ----------
        indent : str
            インデント
        """
        return f"""
{indent}RoomState
{indent}---------
{indent}_value: {self._value}"""


class MyTurn ():
    """自分のターン"""

    def __init__(self, myPiece):
        """生成

        Parameters
        ----------
        myPiece : str
            自分の駒。 "X", "O", "_"
        """

        self._isTrue = myPiece == things.PC_X_LABEL
        """自分の手番か（初回は先手）"""

    @property
    def isTrue(self):
        """真実か？"""
        return self._isTrue

    @property.isTrue
    def isTrue(self, value):
        self._isTrue = value
        # vue1.raiseMyTurnChanged()

    def dump(self, indent):
        """ダンプ

        Parameters
        ----------
        indent : str
            インデント

        Returns
        -------
        str
            ダンプ
        """
        return f"""
{indent}MyTurn
{indent}------
{indent}_isTrue: ${self._isTrue}"""


class GameoverSet():
    """ゲームオーバー集合

    * 自分視点
    """

    @ staticmethod
    @ property
    def none():
        """ゲームオーバーしてません"""
        return 0

    @ staticmethod
    @ property
    def win():
        """勝ち"""
        return 1

    @ staticmethod
    @ property
    def draw():
        """引き分け"""
        return 2

    @ staticmethod
    @ property
    def lose():
        """負け"""
        return 3

    def __init__(self, value):
        """生成

        Parameters
        ----------
        value : int
            値
        """
        self._value = value

    @property
    def value(self):
        """値"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def dump(self, indent):
        """ダンプ

        Parameters
        ----------
        indent : str
            インデント
        """
        if self._value == GameoverSet.none:
            text = "none"
        elif self._value == GameoverSet.won:
            text = "win"
        elif self._value == GameoverSet.draw:
            text = "draw"
        elif self._value == GameoverSet.lost:
            text = "lose"
        else:
            raise ValueError(
                f"[GameoverSet dump] Unexpected value={self._value}")

        return f"""
{indent}GameoverSet
{indent}-----------
{indent}_value: {text}"""


WIN_PATTERN = [
    [things.SQ_0, things.SQ_1, things.SQ_2],
    """
    +---------+
    | *  *  * |
    | .  .  . |
    | .  .  . |
    +---------+
    """

    [things.SQ_3, things.SQ_4, things.SQ_5],
    """
    +---------+
    | .  .  . |
    | *  *  * |
    | .  .  . |
    +---------+
    """

    [things.SQ_6, things.SQ_7, things.SQ_8],
    """
    +---------+
    | .  .  . |
    | .  .  . |
    | *  *  * |
    +---------+
    """

    [things.SQ_0, things.SQ_3, things.SQ_6],
    """
    +---------+
    | *  .  . |
    | *  .  . |
    | *  .  . |
    +---------+
    """

    [things.SQ_1, things.SQ_4, things.SQ_7],
    """
    +---------+
    | .  *  . |
    | .  *  . |
    | .  *  . |
    +---------+
    """

    [things.SQ_2, things.SQ_5, things.SQ_8],
    """
    +---------+
    | .  .  * |
    | .  .  * |
    | .  .  * |
    +---------+
    """

    [things.SQ_0, things.SQ_4, things.SQ_8],
    """
    +---------+
    | *  .  . |
    | .  *  . |
    | .  .  * |
    +---------+
    """

    [things.SQ_2, things.SQ_4, things.SQ_6],
    """
    +---------+
    | .  .  * |
    | .  *  . |
    | *  .  . |
    +---------+
    """
]
"""駒が３つ並んでいるパターン"""


def flipTurn(piece):
    """手番反転

    Returns
    -------
    str
        piece
    """

    if piece == things.PC_X_LABEL:
        return things.PC_O_LABEL
    elif piece == things.PC_O_LABEL:
        return things.PC_X_LABEL

    return piece
