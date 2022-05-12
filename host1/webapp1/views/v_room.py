import json
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers

from webapp1.models.m_room import Room
#    ------- ------ ------        ----
#    1       2      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.forms.f_room import RoomForm
#    ------- ----- ------        --------
#    1       2     3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def listRoom(request):
    """部屋一覧"""
    rooms = Room.objects.all().order_by('id')  # id 順にメンバーを全部取得
    dbRoomJsonStr = serializers.serialize('json', rooms)  # JSON に変換
    # Example:
    # dbRoomJsonStr=[{"model": "webapp1.room", "pk": 2, "fields": {"name": "Elephant", "board": "XOXOXOXOX", "record": "012345678"}}, {"model": "webapp1.room", "pk": 3, "fields": {"name": "Giraffe", "board": "XOXOXOXOX", "record": "012345678"}}, {"model": "webapp1.room", "pk": 5, "fields": {"name": "Gold", "board": "XOXOXOXOX", "record": "012345678"}}]
    # print(f"dbRoomJsonStr={dbRoomJsonStr}")

    dbRoomDoc = json.loads(dbRoomJsonStr)
    # print(f"dbRoomDoc={json.dumps(dbRoomDoc, indent=4)}")
    """
    # Example
    dbRoomDoc=
    [
        {
            "model": "webapp1.room",
            "pk": 2,
            "fields": {
                "name": "Elephant",
                "board": "XOXOXOXOX",
                "record": "012345678"
            }
        },
        ...
    ]
    """

    # 使いやすい形に変換します
    resDoc = dict()
    resDoc["rooms"] = []

    for dbRecord in dbRoomDoc:
        # Example:
        # dbRecord= --> {'model': 'webapp1.room', 'pk': 2, 'fields': {'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}} <--
        # print(f"dbRecord= --> {dbRecord} <--")

        resDoc["rooms"].append(
            {
                "id": dbRecord["pk"],
                "name": dbRecord["fields"]["name"],
                "board": dbRecord["fields"]["board"],
                "record": dbRecord["fields"]["record"],
            }
        )

    # Example:
    # resDoc={'rooms': [{'id': 2, 'name': 'Elephant', 'board': 'XOXOXOXOX', 'record': '012345678'}, {'id': 3, 'name': 'Giraffe', 'board': 'XOXOXOXOX', 'record': '012345678'}, {'id': 5, 'name': 'Gold', 'board': 'XOXOXOXOX', 'record': '012345678'}]}
    # print(f'resDoc={resDoc}')

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # 部屋がいっぱいあるので、名前はホテルとします
        # Vue には、 JSONオブジェクト を渡すのではなく、 JSON文字列 を渡します
        "dj_hotel": json.dumps(resDoc),
        # FIXME 相対パス。 URL を urls.py で変更したいとき、反映されないがどうするか？
        "dj_readRoomPath": "read/",
    }
    # Example:
    # context={'dj_hotel': '{"rooms": [{"id": 2, "name": "Elephant", "board": "XOXOXOXOX", "record": "012345678"}, {"id": 3, "name": "Giraffe", "board": "XOXOXOXOX", "record": "012345678"}, {"id": 5, "name": "Gold", "board": "XOXOXOXOX", "record": "012345678"}]}', 'dj_readRoom': 'rooms/read/'}
    print(f"context={context}")

    return render(request, "rooms/list.html", context)
    #                       ---------------
    #                       1
    # 1. webapp1/templates/rooms/list.html
    #                      ---------------


def readRoom(request, id=id):
    """部屋読取"""
    context = {
        'room': Room.objects.get(pk=id),  # idを指定してメンバーを１人取得
    }
    return render(request, "rooms/read.html", context)
    #                       ---------------
    #                       1
    # 1. webapp1/templates/rooms/read.html
    #                      ---------------


def deleteRoom(request, id=id):
    """部屋削除"""
    template = loader.get_template('rooms/delete.html')

    room = Room.objects.get(pk=id)  # idを指定してメンバーを１人取得
    name = room.name  # 名前だけまだ使う
    room.delete()
    context = {
        'room': {
            'name': name
        }
    }
    return HttpResponse(template.render(context, request))


def upsertRoom(request, id=None):
    """部屋の作成または更新"""

    if id:  # idがあるとき（更新の時）
        # idで検索して、結果を戻すか、404エラー
        room = get_object_or_404(Room, pk=id)
    else:  # idが無いとき（作成の時）
        room = Room()

    # POSTの時（作成であれ更新であれ送信ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():  # バリデーションがOKなら保存
            room = form.save(commit=False)
            room.save()
            return redirect('listRoom')
    else:  # GETの時（フォームを生成）
        form = RoomForm(instance=room)

    # 作成・更新画面を表示
    return render(request, 'rooms/upsert.html', dict(form=form, id=id))
