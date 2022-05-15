import json
from django.core import serializers


from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def get_all_rooms():
    # id順に要素を全部取得
    dbRoomQuerySet = Room.objects.all().order_by('id')
    # roomSet=<QuerySet [<Room: Elephant>, <Room: Giraffe>, <Room: Gold>]>
    print(f"dbRoomQuerySet={dbRoomQuerySet}")

    # JSON 文字列に変換
    dbRoomJsonStr = serializers.serialize('json', dbRoomQuerySet)

    # オブジェクトに変換
    dbRoomDoc = json.loads(dbRoomJsonStr)

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

    return hotelDic
