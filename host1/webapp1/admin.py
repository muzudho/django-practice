# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.contrib import admin
from .models import Member
from .models import Dessert # 追加

# Register your models here.
admin.site.register(Member)
admin.site.register(Dessert) # 追加
