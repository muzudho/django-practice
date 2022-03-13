from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader # 追加

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
