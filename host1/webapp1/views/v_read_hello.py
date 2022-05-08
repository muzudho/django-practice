from django.http import HttpResponse
from django.template import loader


def readHello(request, id=id):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/hello1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
