from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect

from webapp1.models.m_member import Member
#    ------- ------ --------        ------
#    1       2      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.forms.f_member import MemberForm
#    ------- ----- --------        ----------
#    1       2     3               4
# 1. アプリケーション フォルダー名
# 2. Python ファイル名。拡張子抜き
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def listMember(request):
    """メンバー一覧"""
    template = loader.get_template('members/list.html')
    context = {
        'members': Member.objects.all().order_by('id'),  # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))


def readMember(request, id=id):
    """メンバー読取"""
    template = loader.get_template('members/read.html')
    context = {
        'member': Member.objects.get(pk=id),  # idを指定してメンバーを１人取得
    }
    return HttpResponse(template.render(context, request))


def deleteMember(request, id=id):
    """メンバー削除"""
    template = loader.get_template('members/delete.html')

    member = Member.objects.get(pk=id)  # idを指定してメンバーを１人取得
    name = member.name  # 名前だけまだ使う
    member.delete()
    context = {
        'member': {
            'name': name
        }
    }
    return HttpResponse(template.render(context, request))


def upsertMember(request, id=None):
    """メンバーの作成または更新"""

    if id:  # idがあるとき（更新の時）
        # idで検索して、結果を戻すか、404エラー
        member = get_object_or_404(Member, pk=id)
    else:  # idが無いとき（作成の時）
        member = Member()

    # POSTの時（作成であれ更新であれ送信ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():  # バリデーションがOKなら保存
            member = form.save(commit=False)
            member.save()
            return redirect('listMember')
    else:  # GETの時（フォームを生成）
        form = MemberForm(instance=member)

    # 作成・更新画面を表示
    return render(request, 'members/upsert.html', dict(form=form, id=id))
