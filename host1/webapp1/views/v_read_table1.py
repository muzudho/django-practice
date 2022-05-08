from django.http import HttpResponse
from django.template import loader  # 追加


def readDataTable1(request, id=id):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/data-table1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
