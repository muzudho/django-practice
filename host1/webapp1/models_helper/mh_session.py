# See also: 📖[How to get the list of the authenticated users?](https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users)
import json
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.core import serializers
from django.utils import timezone


def get_all_logged_in_users():
    # 接続が切れていないセッションを絞りこみます。
    # ログアウトせず２週間放置しているセッションが含まれる場合があります
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # セッション一覧を、ユーザーID一覧に変換します
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # ユーザーID一覧を使って、ユーザーを絞りこみます
    dbUsersQuerySet = User.objects.filter(id__in=uid_list)
    # users=<QuerySet [<User: kifuwarabe>]>
    # print(f"dbUsersQuerySet={dbUsersQuerySet}")

    # JSON 文字列に変換
    dbUsersJsonStr = serializers.serialize('json', dbUsersQuerySet)
    # print(f"dbUsersJsonStr={dbUsersJsonStr}")

    # オブジェクトに変換
    dbUserDoc = json.loads(dbUsersJsonStr)
    """
web_1  | dbUserDoc=[
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
    # print(f"dbUserDoc={json.dumps(dbUserDoc, indent=4)}")

    # 使いやすい形に変換します
    usersDic = dict()
    for dbUser in dbUserDoc:
        usersDic[dbUser["pk"]] = {
            "pk": dbUser["pk"],
            "last_login": dbUser["fields"]["last_login"],
            "username": dbUser["fields"]["username"],
            "is_active": dbUser["fields"]["is_active"],
        }

    return usersDic
