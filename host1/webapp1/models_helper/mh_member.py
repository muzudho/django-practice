import json
from os import stat
from django.core import serializers


from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MhMember():

    @staticmethod
    def get_all_members():
        """TODO 使ってない？"""

        # id順に要素を全部取得
        dbMemberQuerySet = Member.objects.all().order_by('id')
        # memberSet=<QuerySet [<Member: きふわらね>, <Member: きふわらずさ>, <Member: きふわらかく>, <Member: ほげQ>, <Member: ひょろ>]>
        print(f"dbMemberQuerySet={dbMemberQuerySet}")

        # JSON 文字列に変換
        dbMemberJsonStr = serializers.serialize('json', dbMemberQuerySet)

        # オブジェクトに変換
        dbMemberDoc = json.loads(dbMemberJsonStr)

        # 使いやすい形に変換します
        # 人がいっぱいいるからパーク
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

        return parkDic
