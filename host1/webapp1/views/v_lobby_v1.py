from django.http import HttpResponse
from django.template import loader

from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def visitLobby(request):
    """ロビー（待合室）"""
    template = loader.get_template('lobby/v1/lobby.html')
    #                               -------------------
    #                               1
    # 1. webapp1/templates/lobby/v1/lobby.html
    #                      -------------------

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # 人がいっぱいいるからパーク
        'dj_park': Member.objects.all().order_by('id'),  # id順にメンバーを全部取得
        # 部屋がいっぱいあるからホテル
        'dj_hotel': Room.objects.all().order_by('id'),  # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))
