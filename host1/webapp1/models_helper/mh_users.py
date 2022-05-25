import json
from django.contrib.auth import get_user_model
from django.core import serializers

from webapp1.models.m_user_profile import Profile
#    ------- ------ --------------        -------
#    1       2      3                     4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


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
    # db_users_query_set = Profile.objects.all()
    # db_users_query_set = Profile.objects.all().select_related('user')
    db_users_query_set = User.objects.all()
    # db_users_query_set = User.objects.all().select_related('profile')
    #                                      --------------------------
    #                                      1
    # 1. User クラスを拡張して作った Profile クラスの OneToOneField を指しています

    print(f"db_users_query_set={db_users_query_set}")
    for user2 in db_users_query_set:
        print(f"user2={user2}")

        # JSON 文字列に変換
        #db_user2_json_str = serializers.serialize('json', user2)
        # オブジェクトに変換
        #db_user2_doc = json.loads(db_user2_json_str)
        #print(f"db_user2_doc={json.dumps(db_user2_doc, indent=4)}")

    # JSON 文字列に変換
    db_users_json_str = serializers.serialize('json', db_users_query_set)
    # オブジェクトに変換
    db_user_doc = json.loads(db_users_json_str)
    print(f"db_user_doc={json.dumps(db_user_doc, indent=4)}")

    # 使いやすい形に変換します
    user_dic = dict()
    for db_user in db_user_doc:
        print(f"db_user={db_user}")
        username = db_user["fields"]["username"]
        print(f"db_user['fields']['username']={username}")

        profile = Profile.objects.filter(user__username=username)
        print(f"Profile={profile}")  # QuerySet は中身が見えない
        profile_json_str = serializers.serialize('json', profile)
        # オブジェクトに変換
        profile_doc = json.loads(profile_json_str)
        print(f"profile_doc={json.dumps(profile_doc, indent=4)}")

        user_dic[db_user["pk"]] = {
            "pk": db_user["pk"],
            "last_login": db_user["fields"]["last_login"],
            "username": db_user["fields"]["username"],
            "is_active": db_user["fields"]["is_active"],
            "match_state": profile_doc[0]["fields"]["match_state"],
        }

    return user_dic
