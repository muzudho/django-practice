import json # 追加
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader # 追加
from django.shortcuts import render, get_object_or_404, redirect #追加
from .models import Member #追加
from .forms import MemberForm #追加

def index(request):
    return HttpResponse("Hello, world. You're at the webapp1 index.")

@login_required
def loginUser(request):
    # host1/webapp1/templates/webapp1/login-user.html を取ってきます。 webapp1 が２回出てくるのはテクニックのようです
    template = loader.get_template('webapp1/login-user.html')

    user = request.user
    context = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
    return HttpResponse(template.render(context, request))

def page1(request):
    template = loader.get_template('webapp1/page1.html')
    context = {}
    return HttpResponse(template.render(context, request))

# メンバー一覧
def listMember(request):
    template = loader.get_template('members/list.html')
    context = {
        'members':Member.objects.all().order_by('id'), # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))

# メンバー読取
def readMember(request, id=id):
    template = loader.get_template('members/read.html')
    context = {
        'member':Member.objects.get(pk=id), # idを指定してメンバーを１人取得
    }
    return HttpResponse(template.render(context, request))

# メンバー削除
def deleteMember(request, id=id):
    template = loader.get_template('members/delete.html')
    
    member = Member.objects.get(pk=id) # idを指定してメンバーを１人取得
    name = member.name # 名前だけ取得しておく
    member.delete()
    context = {
        'member': {
            'name' : name
        }
    }
    return HttpResponse(template.render(context, request))

# メンバーの作成または更新
def upsertMember(request, id=None):

    if id: # idがあるとき（更新の時）
        # idで検索して、結果を戻すか、404エラー
        member = get_object_or_404(Member, pk=id)
    else: # idが無いとき（作成の時）
        member = Member()

    # POSTの時（作成であれ更新であれ送信ボタンが押されたとき）
    if request.method == 'POST':
        # フォームを生成
        form = MemberForm(request.POST, instance=member)
        if form.is_valid(): # バリデーションがOKなら保存
            member = form.save(commit=False)
            member.save()
            return redirect('listMember')
    else: # GETの時（フォームを生成）
        form = MemberForm(instance=member)

    # 作成・更新画面を表示
    return render(request, 'members/upsert.html', dict(form=form, id=id))

# Vuetify練習
def readHello(request, id=id):
    template = loader.get_template('vuetify2/hello1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

# Vuetify練習
def readDataTable1(request, id=id):
    template = loader.get_template('vuetify2/data-table1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

# Vuetify練習
def readDataTable2(request):
    template = loader.get_template('vuetify2/data-table2.html')

    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))

# Vuetify練習
def readJsonTextarea1(request):
    template = loader.get_template('vuetify2/json-textarea1.html')

    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))

# （追加）Vuetify練習
def readDataTable2b(request):
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template('vuetify2/data-table2.html')
    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))
