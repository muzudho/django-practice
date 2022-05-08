from django.forms import ModelForm

from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MemberForm(ModelForm):
    class Meta:
        model = Member  # モデル指定
        fields = ('name', 'email', 'age',)  # フィールド指定
