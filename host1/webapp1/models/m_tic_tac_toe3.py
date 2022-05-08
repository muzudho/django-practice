# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models


class TicTacToeRoom3(models.Model):
    """Tic-tac-toe3の部屋のモデル"""

    # プロパティの仕様を決める感じで

    # 部屋名
    # -----
    # Example: Elephant
    room = models.CharField('部屋名', max_length=25)

    # 盤面
    # ----
    # Example: ..O.X.X..
    # +--+--+--+
    # |  |  | O|
    # +--+--+--+
    # |  | X|  |
    # +--+--+--+
    # | X|  |  |
    # +--+--+--+
    board = models.CharField('盤面', max_length=9)

    # 棋譜
    # ----
    # Example: 426
    record = models.CharField('棋譜', max_length=9)

    # このオブジェクトを文字列にしたとき返るもの
    def __str__(self):
        return self.name
