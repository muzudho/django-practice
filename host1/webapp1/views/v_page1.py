from django.http import HttpResponse
from django.template import loader  # 追加


def page1(request):
    template = loader.get_template('webapp1/page1.html')
    context = {}
    return HttpResponse(template.render(context, request))
