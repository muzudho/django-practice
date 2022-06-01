from django.http import HttpResponse
from django.template import loader


def render_page1(request):
    template = loader.get_template('webapp1/practice/page1.html')
    context = {}
    return HttpResponse(template.render(context, request))
