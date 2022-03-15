from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader # 追加
from django.shortcuts import render, get_object_or_404 #追加
from .models import Member #追加

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
def memberList(request):
    template = loader.get_template('members/list.html')
    context = {
        'members':Member.objects.all().order_by('id'), # id順にメンバーを全部取得
    }
    return HttpResponse(template.render(context, request))

# メンバー読取
def memberRead(request, id=id):
    member = get_object_or_404(Member, pk=id)
    return render(request, 'members/read.html', {'member':member})
