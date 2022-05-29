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
    def get_user_dic():
        """会員登録ユーザー一覧"""
        User = get_user_model()

        # 会員登録ユーザー一覧
        # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
        user_table_qs = User.objects.all()  # QuerySet
        print(f"user_table_qs={user_table_qs}")
        user_table_json = serializers.serialize('json', user_table_qs)
        user_table_doc = json.loads(user_table_json)  # オブジェクト
        print(f"user_table_doc={json.dumps(user_table_doc, indent=4)}")

        # 使いやすい形に変換します
        user_dic = dict()
        for user_rec in user_table_doc:
            user_dic[user_rec["pk"]] = {
                "pk": user_rec["pk"],
                "last_login": user_rec["fields"]["last_login"],
                "username": user_rec["fields"]["username"],
                "is_active": user_rec["fields"]["is_active"],
            }

        return user_dic

    @staticmethod
    def get_user_dic_v2():
        """会員登録ユーザー一覧 v2"""
        User = get_user_model()

        # 会員登録ユーザー一覧
        # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
        user_table_qs = User.objects.all().select_related('profile')  # QuerySet
        #                                 --------------------------
        #                                 1
        # 1. これを付けて何が起こっているか分からないが、サンプルでよく付けているのを見かけるので真似する。外しても動く。
        #    User クラスを拡張して作った Profile クラスの OneToOneField フィールドの名前を指しています
        # print(f"user_table_qs={user_table_qs}")
        #
        user_table_json = serializers.serialize('json', user_table_qs)
        user_table_doc = json.loads(user_table_json)
        # print(f"user_table_doc={json.dumps(user_table_doc, indent=4)}")

        # 使いやすい形に変換します
        user_dic = dict()
        for user_rec in user_table_doc:  # User Record
            # print(f"user_rec={user_rec}")
            username = user_rec["fields"]["username"]
            # print(f"user_rec['fields']['username']={username}")

            # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
            profile_table_qs = Profile.objects.filter(  # QuerySet
                #                             -------
                #                             1
                user__username=username)
            # 1. filter ならインスタンスが返ってくる。 get なら文字列表現が返ってくる
            # QuerySet は中身が見えないので JSON にダンプするのが定番
            # print(f"Profile={profile_table_qs}")
            #
            profile_table_json = serializers.serialize(
                'json', profile_table_qs)
            profile_table_doc = json.loads(profile_table_json)  # オブジェクト
            # print(f"profile_table_doc={json.dumps(profile_table_doc, indent=4)}")

            user_dic[user_rec["pk"]] = {
                "pk": user_rec["pk"],
                "last_login": user_rec["fields"]["last_login"],
                "username": user_rec["fields"]["username"],
                "is_active": user_rec["fields"]["is_active"],

                "match_state": profile_table_doc[0]["fields"]["match_state"],
                #                               ---
                #                               1
                # 1. 先頭の1件を取っている
            }

        return user_dic

    @staticmethod
    def get_name_by_id(id):
        """ユーザーIDを使って、ユーザーを絞りこみます"""

        # ２段階変換: 問合せ結果（QuerySet） ----> JSON文字列 ----> オブジェクト
        user_table_qs = User.objects.filter(id=id)  # QuerySet
        user_table_json = serializers.serialize('json', user_table_qs)
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
