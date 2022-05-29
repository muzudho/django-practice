import json
from django.http import HttpResponse
from django.template import loader

from webapp1.models_helper.mh_room import get_all_rooms
#    ------- ------------- -------        -------------
#    1       2             3              4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 関数名


from webapp1.models_helper.mh_session import MhSession
#    ------- ------------- ----------        ---------
#    1       2             3                 4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def render_lobby(request):
    """ロビー（待合室）"""
    template = loader.get_template('webapp1/lobby/v1/lobby.html')
    #                               ---------------------------
    #                               1
    # 1. webapp1/templates/webapp1/lobby/v1/lobby.html
    #                      ---------------------------

    # 部屋の一覧
    hotelDic = get_all_rooms()

    # ユーザーの一覧
    usersDic = MhSession.get_all_logged_in_users()

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # 部屋がいっぱいあるからホテル
        'dj_hotel': json.dumps(hotelDic),
        # 人がいっぱいいるからパーク
        'dj_park': json.dumps(usersDic),
        # FIXME 相対パス。 URL を urls.py で変更したいとき、反映されないがどうするか？
        "dj_pathOfHome": "home/v2/",
        "dj_pathOfRoomsRead": "rooms/read/",
    }

    return HttpResponse(template.render(context, request))
