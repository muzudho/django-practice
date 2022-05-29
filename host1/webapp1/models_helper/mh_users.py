import json
from django.contrib.auth import get_user_model
from django.core import serializers
from django.contrib.auth.models import User

from webapp1.models.m_user_profile import Profile
#    ------- ------ --------------        -------
#    1       2      3                     4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class MhUser():

    @staticmethod
    def get_name_by_id(id):
        """ユーザーIDを使って、ユーザーを絞りこみます"""

        # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
        user_table_qs = User.objects.filter(id=id)  # QuerySet
        user_table_json = serializers.serialize(
            'json', user_table_qs)  # JSON 文字列
        # print(f"user_table_json={user_table_json}")

        user_table_doc = json.loads(user_table_json)  # オブジェクト
        print(f"user_table_doc={json.dumps(user_table_doc, indent=4)}")

        if len(user_table_doc) < 1:
            # 該当なしは空文字列と決めておきます
            return ""

        return user_table_doc[0]["fields"]["username"]
        #                    ---
        #                    1
        # 1. 先頭の要素


def get_user_dic():
    """会員登録ユーザー一覧"""
    User = get_user_model()

    # 会員登録ユーザー一覧
    db_users_query_set = User.objects.all()
    print(f"db_users_query_set={db_users_query_set}")

    # JSON 文字列に変換
    db_users_json_str = serializers.serialize('json', db_users_query_set)
    # オブジェクトに変換
    db_user_doc = json.loads(db_users_json_str)
    print(f"db_user_doc={json.dumps(db_user_doc, indent=4)}")

    # 使いやすい形に変換します
    user_dic = dict()
    for db_user in db_user_doc:
        user_dic[db_user["pk"]] = {
            "pk": db_user["pk"],
            "last_login": db_user["fields"]["last_login"],
            "username": db_user["fields"]["username"],
            "is_active": db_user["fields"]["is_active"],
        }

    return user_dic


def get_user_dic_v2():
    """会員登録ユーザー一覧 v2"""
    User = get_user_model()

    # 会員登録ユーザー一覧
    user_table_query_set = User.objects.all().select_related('profile')
    #                                         -------------------------
    #                                         1
    # 1. これを付けて何が起こっているか分からないが、サンプルでよく付けているのを見かけるので真似する。外しても動く。
    #    User クラスを拡張して作った Profile クラスの OneToOneField フィールドの名前を指しています
    # print(f"user_table_query_set={user_table_query_set}")

    # ２段階変換　QuerySet ----> JSON文字列 ----> オブジェクト
    user_table_json_str = serializers.serialize('json', user_table_query_set)
    user_table_doc = json.loads(user_table_json_str)
    # print(f"user_table_doc={json.dumps(user_table_doc, indent=4)}")

    # 使いやすい形に変換します
    user_dic = dict()
    for user_record_doc in user_table_doc:
        # print(f"user_record_doc={user_record_doc}")
        username = user_record_doc["fields"]["username"]
        # print(f"user_record_doc['fields']['username']={username}")

        profile_table_query_set = Profile.objects.filter(
            user__username=username)
        #                         ------
        #                         1
        # 1. filter ならインスタンスが返ってくる。 get なら文字列表現が返ってくる
        # QuerySet は中身が見えないので JSON にダンプするのが定番
        # print(f"Profile={profile_table_query_set}")

        # ２段階変換　QuerySet ----> JSON文字列 ----> オブジェクト
        profile_table_json_str = serializers.serialize(
            'json', profile_table_query_set)
        profile_table_doc = json.loads(profile_table_json_str)
        # print(f"profile_table_doc={json.dumps(profile_table_doc, indent=4)}")

        user_dic[user_record_doc["pk"]] = {
            "pk": user_record_doc["pk"],
            "last_login": user_record_doc["fields"]["last_login"],
            "username": user_record_doc["fields"]["username"],
            "is_active": user_record_doc["fields"]["is_active"],

            "match_state": profile_table_doc[0]["fields"]["match_state"],
            #                               ---
            #                               1
            # 1. 先頭の1件を取っている
        }

    return user_dic
