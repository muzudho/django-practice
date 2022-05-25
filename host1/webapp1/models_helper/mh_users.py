import json
from django.contrib.auth import get_user_model
from django.core import serializers


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
