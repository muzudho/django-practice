from django.forms import ModelForm
from .models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member # モデル指定
        fields = ('name','email','age',) # フィールド指定
