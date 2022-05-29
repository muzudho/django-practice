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

        # ２段階変換: 問合せ結果（QuerySet）id順 ----> JSON文字列 ----> オブジェクト
        member_table_qs = Member.objects.all().order_by('id')  # 問合せ結果（QuerySet）id順
        # memberSet=<QuerySet [<Member: きふわらね>, <Member: きふわらずさ>, <Member: きふわらかく>, <Member: ほげQ>, <Member: ひょろ>]>
        print(f"member_table_qs={member_table_qs}")
        member_table_json = serializers.serialize('json', member_table_qs)
        member_table_doc = json.loads(member_table_json)  # オブジェクト

        # 使いやすい形に変換します
        # 人がいっぱいいるからパーク
        park_dic = dict()
        for member_rec in member_table_doc:  # Member record
            # Example:
            # member_rec= --> {'model': 'webapp1.member', 'pk': 1, 'fields': {'name': 'きふわらね', 'email': 'kifuwarane@example.com', 'age': 8, 'stateInPark': 0}} <--
            print(f"member_rec= --> {member_rec} <--")

            park_dic[member_rec["pk"]] = {
                "pk": member_rec["pk"],
                "name": member_rec["fields"]["name"],
                "board": member_rec["fields"]["email"],
                "record": member_rec["fields"]["age"],
                "record": member_rec["fields"]["stateInPark"],
            }

        return park_dic
