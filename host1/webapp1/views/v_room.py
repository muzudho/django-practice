from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect

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
    template = loader.get_template('rooms/list.html')
    context = {
        'rooms': Room.objects.all().order_by('id'),  # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))


def readRoom(request, id=id):
    """部屋読取"""
    template = loader.get_template('rooms/read.html')
    context = {
        'room': Room.objects.get(pk=id),  # idを指定してメンバーを１人取得
    }
    return HttpResponse(template.render(context, request))


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
