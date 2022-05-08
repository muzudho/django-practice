import json  # 追加
from django.http import HttpResponse
from django.template import loader  # 追加


def readDataTable2(request):
    """Vuetify練習"""
    template = loader.get_template('vuetify2/data-table2.html')

    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))
