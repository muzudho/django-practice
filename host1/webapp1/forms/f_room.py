from django.forms import ModelForm

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class RoomForm(ModelForm):
    class Meta:
        model = Room  # モデル指定
        fields = ('name', 'board', 'record',)  # フィールド指定
