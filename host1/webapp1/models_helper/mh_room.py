import json
from os import stat
from django.core import serializers


from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MhRoom():

    @staticmethod
    def get_all_rooms_as_dic():
        # id順に要素を全部取得
        room_table_qs = Room.objects.all().order_by('id')
        # roomSet=<QuerySet [<Room: Elephant>, <Room: Giraffe>, <Room: Gold>]>
        print(f"room_table_qs={room_table_qs}")

        # JSON 文字列に変換
        room_table_json = serializers.serialize('json', room_table_qs)

        # オブジェクトに変換
        room_table_doc = json.loads(room_table_json)

        # 使いやすい形に変換します
        room_dic = dict()
        for dbRoom in room_table_doc:

            # Example:
            # dbRoom= --> {'model': 'webapp1.room', 'pk': 2, 'fields': {'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}} <--
            print(f"dbRoom= --> {dbRoom} <--")

            room_dic[dbRoom["pk"]] = {
                "pk": dbRoom["pk"],
                "name": dbRoom["fields"]["name"],
                "board": dbRoom["fields"]["board"],
                "record": dbRoom["fields"]["record"],
            }

        return room_dic
