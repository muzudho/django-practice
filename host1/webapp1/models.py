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
