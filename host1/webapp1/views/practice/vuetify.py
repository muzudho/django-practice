import json
from django.http import HttpResponse
from django.template import loader


def readDataTable2(request):
    """Vuetify練習"""
    template = loader.get_template(
        'webapp1/practice/vuetify-data-table2.html')
    #                     ------------------------
    #                     1
    # 1. host1/webapp1/templates/webapp1/practice/vuetify-data-table2.html を取ってきます。
    #                            -----------------------------------------

    with open('webapp1/static/webapp1/practice/vuetify-desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readJsonTextarea1(request):
    """Vuetify練習"""
    template = loader.get_template(
        'webapp1/practice/vuetify-json-textarea1.html')
    #    --------------------------------------------
    #    1
    # 1. host1/webapp1/templates/webapp1/practice/vuetify-json-textarea1.html を取ってきます。
    #                            --------------------------------------------

    with open('webapp1/static/webapp1/practice/vuetify-desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2o2(request):
    """Vuetify練習"""
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template(
        'webapp1/practice/vuetify-data-table2.html')
    #    -----------------------------------------
    #    1
    # 1. host1/webapp1/templates/webapp1/practice/vuetify-data-table2.html を取ってきます。
    #                            -----------------------------------------

    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))
