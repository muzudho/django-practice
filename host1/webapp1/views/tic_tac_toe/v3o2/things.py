# +--------
# | 駒
# |

# PC は Piece （駒）の略です。
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

# |
# | 駒
# +--------

# +--------
# | 盤
# |

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


class Board ():
    def __init__(self):
        """"""

        self._squares = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY,
                         PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY]
        """各マス"""

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
        return self._squares[sq]

    def setPiece(self, sq, piece):
        """盤上のマスに駒を上書きします

        Parameters
        ----------
        sq : int
            マス番号
        piece : str
            駒
        """
        self._squares[sq] = piece

    def dump(self, indent):
        """ダンプ"""
        return f"""
{indent}Board
{indent}-----
{indent}_squares: {self._squares}"""


# | 盤
# |
# +--------

# +--------
# | 棋譜
# |


class Record ():
    def __init__(self):
        self._squares = []

    def push(self, sq):
        """追加

        Parameters
        ----------
        sq : int
            駒を置いた場所
        """
        self._squares.append(sq)

    def pop(self):
        self._squares.pop()

    @property
    def length(self):
        return len(self._squares)

    def dump(self, indent):
        """ダンプ"""
        return f"""
{indent}Record
{indent}------
{indent}_squares: ${self._squares}"""


# | 棋譜
# |
# +--------
