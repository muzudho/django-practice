import json
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader

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


def render_list_room(request):
    """部屋一覧"""

    # ２段階変換: roomテーブルid順 ----> JSON文字列 ----> オブジェクト
    room_table_qs = Room.objects.all().order_by('id')  # Query Set
    room_table_json = serializers.serialize('json', room_table_qs)  # JSON 文字列
    # print(f"room_table_json={room_table_json}")

    room_table_doc = json.loads(room_table_json)  # オブジェクト
    # print(f"room_table_doc={json.dumps(room_table_doc, indent=4)}")
    """
    # Example
    room_table_doc=
    [
        {
            "model": "webapp1.room",
            "pk": 2,
            "fields": {
                "name": "Elephant",
                "sente_id": 1,
                "gote_id": 2,
                "board": "XOXOXOXOX",
                "record": "012345678"
            }
        },
        ...中略...
    ]
    """

    # 使いやすい形に変換します
    room_list = []

    for room_rec in room_table_doc:  # Room record
        # print(f"room_rec= --> {room_rec} <--")

        room_list.append(
            {
                "id": room_rec["pk"],
                "name": room_rec["fields"]["name"],
                "sente_id": room_rec["fields"]["sente_id"],
                "gote_id": room_rec["fields"]["gote_id"],
                "board": room_rec["fields"]["board"],
                "record": room_rec["fields"]["record"],
            }
        )

    # print(f'room_list={room_list}')

    context = {
        # "dj_" は 「Djangoがレンダーに埋め込む変数」 の目印
        # Vue には、 JSONオブジェクト を渡すのではなく、 JSON文字列 を渡します
        "dj_room_array": json.dumps(room_list),
        # FIXME URL を urls.py で変更しても、こちらに反映されないが、どうするか？
        "dj_read_room_path": "/rooms/read/",
    }
    # print(f"context={context}")

    return render(request, "webapp1/rooms/list.html", context)
    #                       -----------------------
    #                       1
    # 1. webapp1/templates/webapp1/rooms/list.html
    #                      -----------------------


def render_read_room(request, id=id):
    """部屋読取"""
    context = {
        'room': Room.objects.get(pk=id),  # idを指定してメンバーを１人取得
    }
    return render(request, "webapp1/rooms/read.html", context)
    #                       -----------------------
    #                       1
    # 1. webapp1/templates/webapp1/rooms/read.html
    #                      -----------------------


def render_delete_room(request, id=id):
    """部屋削除"""
    template = loader.get_template('webapp1/rooms/delete.html')
    #                               -------------------------
    #                               1
    # 1. webapp1/templates/webapp1/rooms/delete.html
    #                      -------------------------

    room = Room.objects.get(pk=id)  # idを指定してメンバーを１人取得
    name = room.name  # 名前だけまだ使う
    room.delete()
    context = {
        'room': {
            'name': name
        }
    }
    return HttpResponse(template.render(context, request))


def render_upsert_room(request, id=None):
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
    return render(request, 'webapp1/rooms/upsert.html', dict(form=form, id=id))
    #                       -------------------------
    #                       1
    # 1. webapp1/templates/webapp1/rooms/upsert.html
    #                      -------------------------
