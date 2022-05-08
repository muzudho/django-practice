# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models


class Dessert(models.Model):
    """デザート"""

    # プロパティの仕様を決める感じで
    name = models.CharField('Name', max_length=32)
    calories = models.IntegerField('Calories', blank=True, default=0)
    fat = models.FloatField('Fat (g)', blank=True, default=0)
    carbs = models.IntegerField('Carbs (g)', blank=True, default=0)
    protein = models.FloatField('Protein (g)', blank=True, default=0)
    iron = models.CharField('Iron (%)', max_length=4, blank=True)

    # このオブジェクトを文字列にしたとき返るもの
    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return self.name
