# ゲームオーバー判定
#
# * 自分視点
GAMEOVER_NONE = 0
"""ゲームオーバーしてません"""

GAMEOVER_WIN = 1
"""勝ち"""

GAMEOVER_DRAW = 2
"""引き分け"""

GAMEOVER_LOSE = 3
"""負け"""

# PC は Piece （駒、石、などの意味）の略です。
PC_EMPTY = 0
"""Pieceがないことを表します"""

PC_X = 1
"""先手"""

PC_O = 2
"""後手"""

# ラベル
PC_EMPTY_LABEL = ""
"""空きマス"""

PC_X_LABEL = "X"
"""先手"""

PC_O_LABEL = "O"
"""後手"""

BOARD_AREA = 9
"""盤上の升の数"""

SQ_0 = 0
"""SQ is square
+---------+
| 0  1  2 |
| 3  4  5 |
| 6  7  8 |
+---------+
"""

SQ_1 = 1
"""1のマス"""

SQ_2 = 2
"""2のマス"""

SQ_3 = 3
"""3のマス"""

SQ_4 = 4
"""4のマス"""

SQ_5 = 5
"""5のマス"""

SQ_6 = 6
"""6のマス"""

SQ_7 = 7
"""7のマス"""

SQ_8 = 8
"""8のマス"""

WIN_PATTERN = [
    [SQ_0, SQ_1, SQ_2],
    """
    +---------+
    | *  *  * |
    | .  .  . |
    | .  .  . |
    +---------+
    """

    [SQ_3, SQ_4, SQ_5],
    """
    +---------+
    | .  .  . |
    | *  *  * |
    | .  .  . |
    +---------+
    """

    [SQ_6, SQ_7, SQ_8],
    """
    +---------+
    | .  .  . |
    | .  .  . |
    | *  *  * |
    +---------+
    """

    [SQ_0, SQ_3, SQ_6],
    """
    +---------+
    | *  .  . |
    | *  .  . |
    | *  .  . |
    +---------+
    """

    [SQ_1, SQ_4, SQ_7],
    """
    +---------+
    | .  *  . |
    | .  *  . |
    | .  *  . |
    +---------+
    """

    [SQ_2, SQ_5, SQ_8],
    """
    +---------+
    | .  .  * |
    | .  .  * |
    | .  .  * |
    +---------+
    """

    [SQ_0, SQ_4, SQ_8],
    """
    +---------+
    | *  .  . |
    | .  *  . |
    | .  .  * |
    +---------+
    """

    [SQ_2, SQ_4, SQ_6],
    """
    +---------+
    | .  .  * |
    | .  *  . |
    | *  .  . |
    +---------+
    """
]
"""石が３つ並んでいるパターン"""


def flipTurn(piece):
    """手番反転

    Returns
    -------
    str
        piece
    """

    if piece == PC_X_LABEL:
        return PC_O_LABEL
    elif piece == PC_O_LABEL:
        return PC_X_LABEL

    return piece