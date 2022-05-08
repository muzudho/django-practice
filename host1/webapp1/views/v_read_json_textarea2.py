import json
from django.http import HttpResponse
from django.template import loader


def readJsonTextarea2(request):
    """（追加）"""
    template = loader.get_template('vuetify2/json-textarea2.html')

    with open('webapp1/static/desserts-placeholder.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))
