from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader # 追加

def index(request):
    return HttpResponse("Hello, world. You're at the webapp1 index.")

@login_required
def loginUserList(request):
    # host1/webapp1/templates/webapp1/login-user-list.html を取ってきます
    template = loader.get_template('webapp1/login-user-list.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
