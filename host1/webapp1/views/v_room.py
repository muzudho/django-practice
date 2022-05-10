from django.http import HttpResponse
from django.template import loader

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def listRoom(request):
    """部屋一覧"""
    template = loader.get_template('rooms/list.html')
    context = {
        'rooms': Room.objects.all().order_by('id'),  # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))


def readRoom(request, id=id):
    """部屋読取"""
    template = loader.get_template('rooms/read.html')
    context = {
        'room': Room.objects.get(pk=id),  # idを指定してメンバーを１人取得
    }
    return HttpResponse(template.render(context, request))


def deleteRoom(request, id=id):
    """部屋削除"""
    template = loader.get_template('rooms/delete.html')

    room = Room.objects.get(pk=id)  # idを指定してメンバーを１人取得
    name = room.name  # 名前だけまだ使う
    room.delete()
    context = {
        'room': {
            'name': name
        }
    }
    return HttpResponse(template.render(context, request))
