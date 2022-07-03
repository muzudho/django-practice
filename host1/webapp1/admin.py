# See also: https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92
from django.contrib import admin
from .models.m_room import Room
from .models.m_user_profile import Profile

# Register your models here.
admin.site.register(Room)
admin.site.register(Profile)
