import json  # 追加
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template import loader  # 追加
from django.shortcuts import render, get_object_or_404, redirect  # 追加
from .models import Member, Dessert  # 追加
from .forms import MemberForm  # 追加


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
    name = member.name  # 名前だけ取得しておく
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


def readHello(request, id=id):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/hello1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def readDataTable1(request, id=id):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/data-table1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def readDataTable2(request):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/data-table2.html')

    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readJsonTextarea1(request):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/json-textarea1.html')

    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2b(request):
    """（追加）Vuetify練習"""
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template('vuetify2/data-table2.html')
    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))


def readJsonResponse1(request):
    """（追加）JSONでの応答練習"""
    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    return JsonResponse(doc)


def readJsonTextarea2(request):
    """（追加）"""
    template = loader.get_template('vuetify2/json-textarea2.html')

    with open('webapp1/static/desserts-placeholder.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2c(request):
    """（追加）"""
    form1Textarea1 = request.POST["textarea1"]
    doc = json.loads(form1Textarea1)  # Dessert

    record = Dessert(
        name=doc["name"],
        calories=doc["calories"],
        fat=doc["fat"],
        carbs=doc["carbs"],
        protein=doc["protein"],
        iron=doc["iron"])
    record.save()

    doc2 = {
        'result': "Success"
    }
    return JsonResponse(doc2)


def indexOfTicTacToe1(request):
    """（追加） For Tic-tac-toe"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe1/{room_name}/?&mypiece={myPiece}')
    return render(request, "tic-tac-toe1/index.html", {})


def playGameOfTicTacToe1(request, room_name):
    """（追加） For Tic-tac-toe"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe1/game.html", context)
