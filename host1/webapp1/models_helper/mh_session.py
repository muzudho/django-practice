# See also: 📖[How to get the list of the authenticated users?](https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users)
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
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
    return User.objects.filter(id__in=uid_list)
