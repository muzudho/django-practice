# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.db import models

# 任意のオブジェクトの仕様を決める感じで
class Member(models.Model):

    # プロパティの仕様を決める感じで
    name = models.CharField('氏名', max_length=255)
    email = models.CharField('E-Mail', max_length=255)
    age = models.IntegerField('年齢', blank=True, default=0)

    # このオブジェクトを文字列にしたとき返るもの
    def __str__(self):
        return self.name

class Dessert(models.Model):

    name = models.CharField('Name', max_length=32)
    calories = models.IntegerField('Calories', blank=True, default=0)
    fat = models.FloatField('Fat (g)', blank=True, default=0)
    carbs = models.IntegerField('Carbs (g)', blank=True, default=0)
    protein = models.FloatField('Protein (g)', blank=True, default=0)
    iron = models.CharField('Iron (%)', max_length=4, blank=True)

    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return self.name
