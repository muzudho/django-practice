import json
from django.http import HttpResponse
from django.template import loader

from webapp1.models_helper.mh_room import MhRoom
#    ------- ------------- -------        ------
#    1       2             3              4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


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
    # 1. host1/webapp1/templates/webapp1/lobby/v1/lobby.html
    #                            ---------------------------

    # 部屋の一覧
    room_dic = MhRoom.get_all_rooms_as_dic()

    # ユーザーの一覧
    user_dic = MhSession.get_all_logged_in_users()

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        'dj_room_dic': json.dumps(room_dic),
        'dj_user_dic': json.dumps(user_dic),
        # FIXME URL を urls.py で変更しても、こちらに反映されないが、どうするか？
        "dj_path_of_home": "/home/v1/",
        "dj_path_of_rooms_read": "/rooms/read/",
    }

    return HttpResponse(template.render(context, request))
