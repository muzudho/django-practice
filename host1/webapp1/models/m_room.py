# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models


class Room(models.Model):
    """部屋のモデル"""

    # プロパティの仕様を決める感じで

    # 部屋名
    # -----
    # Example: Elephant
    name = models.CharField('部屋名', max_length=25)

    # 対局者_先手Id
    # ------------
    # Example: 1
    sente_id = models.IntegerField('対局者_先手Id', null=True, blank=True)

    # 対局者_後手Id
    # ------------
    # Example: 2
    gote_id = models.IntegerField('対局者_後手Id', null=True, blank=True)

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

    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return self.name
