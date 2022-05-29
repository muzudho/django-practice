# See also: 📖[How to get the list of the authenticated users?](https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users)
import json
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core import serializers
from django.utils import timezone


class MhSession():

    @staticmethod
    def get_all_logged_in_users():
        # 接続が切れていないセッションを絞りこみます。
        # ログアウトせず２週間放置しているセッションが含まれる場合があります
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []

        # セッション一覧を、ユーザーID一覧に変換します
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))

        # ２段階変換: 問合せ結果（QuerySet）id絞りこみ ----> JSON文字列 ----> オブジェクト
        user_table_qs = User.objects.filter(id__in=uid_list)  # QuerySet
        # users=<QuerySet [<User: kifuwarabe>]>
        # print(f"user_table_qs={user_table_qs}")
        user_table_json = serializers.serialize('json', user_table_qs)
        user_table_doc = json.loads(user_table_json)  # オブジェクトに変換
        """
web_1  | user_table_doc=[
web_1  |     {
web_1  |         "model": "auth.user",
web_1  |         "pk": 1,
web_1  |         "fields": {
web_1  |             "password": "pbkdf2_sha256$260000$tOSdFO6BqvafBgtFgE1qYS$+rv007MKnAy8j+krixlQuogvi46Xl8fZf87xn4lAU+0=",
web_1  |             "last_login": "2022-05-14T03:09:21.968Z",
web_1  |             "is_superuser": false,
web_1  |             "username": "kifuwarabe",
web_1  |             "first_name": "",
web_1  |             "last_name": "",
web_1  |             "email": "muzudho1@gmail.com",
web_1  |             "is_staff": false,
web_1  |             "is_active": true,
web_1  |             "date_joined": "2022-03-13T05:45:26.368Z",
web_1  |             "groups": [],
web_1  |             "user_permissions": []
web_1  |         }
web_1  |     }
web_1  | ]
"""
        # print(f"user_table_doc={json.dumps(user_table_doc, indent=4)}")

        # 使いやすい形に変換します
        user_dic = dict()
        for user_rec in user_table_doc:  # User Record
            user_dic[user_rec["pk"]] = {
                "pk": user_rec["pk"],
                "last_login": user_rec["fields"]["last_login"],
                "username": user_rec["fields"]["username"],
                "is_active": user_rec["fields"]["is_active"],
            }

        return user_dic
