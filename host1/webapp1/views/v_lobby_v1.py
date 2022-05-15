import json
from django.core import serializers
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

    # id順に要素を全部取得
    dbRoomQuerySet = Room.objects.all().order_by('id')
    dbMemberQuerySet = Member.objects.all().order_by('id')
    # roomSet=<QuerySet [<Room: Elephant>, <Room: Giraffe>, <Room: Gold>]>
    print(f"dbRoomQuerySet={dbRoomQuerySet}")
    # memberSet=<QuerySet [<Member: きふわらね>, <Member: きふわらずさ>, <Member: きふわらかく>, <Member: ほげQ>, <Member: ひょろ>]>
    print(f"dbMemberQuerySet={dbMemberQuerySet}")

    # JSON 文字列に変換
    dbRoomJsonStr = serializers.serialize('json', dbRoomQuerySet)
    dbMemberJsonStr = serializers.serialize('json', dbMemberQuerySet)

    # オブジェクトに変換
    dbRoomDoc = json.loads(dbRoomJsonStr)
    dbMemberDoc = json.loads(dbMemberJsonStr)

    # 使いやすい形に変換します
    hotelDic = dict()
    for dbRoom in dbRoomDoc:

        # Example:
        # dbRoom= --> {'model': 'webapp1.room', 'pk': 2, 'fields': {'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}} <--
        print(f"dbRoom= --> {dbRoom} <--")

        hotelDic[dbRoom["pk"]] = {
            "pk": dbRoom["pk"],
            "name": dbRoom["fields"]["name"],
            "board": dbRoom["fields"]["board"],
            "record": dbRoom["fields"]["record"],
        }

    # 使いやすい形に変換します
    parkDic = dict()
    for dbMember in dbMemberDoc:
        # Example:
        # dbMember= --> {'model': 'webapp1.member', 'pk': 1, 'fields': {'name': 'きふわらね', 'email': 'kifuwarane@example.com', 'age': 8, 'stateInPark': 0}} <--
        print(f"dbMember= --> {dbMember} <--")

        parkDic[dbMember["pk"]] = {
            "pk": dbMember["pk"],
            "name": dbMember["fields"]["name"],
            "board": dbMember["fields"]["email"],
            "record": dbMember["fields"]["age"],
            "record": dbMember["fields"]["stateInPark"],
        }

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # 人がいっぱいいるからパーク
        'dj_park': json.dumps(parkDic),
        # 部屋がいっぱいあるからホテル
        'dj_hotel': json.dumps(hotelDic),
    }
    return HttpResponse(template.render(context, request))
