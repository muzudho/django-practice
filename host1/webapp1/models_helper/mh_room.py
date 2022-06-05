import json
from django.core import serializers


from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MhRoom():
    """部屋モデルヘルパー"""

    @staticmethod
    def get_all_rooms_as_dic():
        # ２段階変換: 問合せ結果（QuerySet）id順 ----> JSON文字列 ----> オブジェクト
        room_table_qs = Room.objects.all().order_by('id')  # QuerySet
        # roomSet=<QuerySet [<Room: Elephant>, <Room: Giraffe>, <Room: Gold>]>
        print(f"room_table_qs={room_table_qs}")
        room_table_json = serializers.serialize('json', room_table_qs)
        room_table_doc = json.loads(room_table_json)  # オブジェクト

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
