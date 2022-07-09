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


class RoomView():
    """部屋"""

    @staticmethod
    def render_upsert(request, id=None):
        """作成または更新のページ"""

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
        # 1. host1/webapp1/templates/webapp1/rooms/upsert.html
        #                            -------------------------
