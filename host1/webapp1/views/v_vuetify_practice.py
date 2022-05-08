import json  # 追加
from django.http import HttpResponse
from django.template import loader


def readHello(request, id=id):
    """Vuetify練習"""

    template = loader.get_template('vuetify-practice/hello1.html')
    #                               ----------------------------
    #                               1
    # 1. host1/webapp1/templates/vuetify-practice/hello1.html を取ってきます。
    #                            ----------------------------

    context = {
    }

    return HttpResponse(template.render(context, request))


def readDataTable1(request, id=id):
    """Vuetify練習"""

    template = loader.get_template('vuetify-practice/data-table1.html')
    #                               ---------------------------------
    #                               1
    # 1. host1/webapp1/templates/vuetify-practice/data-table1.html を取ってきます。
    #                            ---------------------------------

    context = {
    }

    return HttpResponse(template.render(context, request))


def readDataTable2(request):
    """Vuetify練習"""
    template = loader.get_template('vuetify-practice/data-table2.html')
    #                               ---------------------------------
    #                               1
    # 1. host1/webapp1/templates/vuetify-practice/data-table2.html を取ってきます。
    #                            ---------------------------------

    with open('webapp1/static/vuetify-practice/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readJsonTextarea1(request):
    """Vuetify練習"""
    template = loader.get_template('vuetify-practice/json-textarea1.html')
    #                               ------------------------------------
    #                               1
    # 1. host1/webapp1/templates/vuetify-practice/json-textarea1.html を取ってきます。
    #                            ------------------------------------

    with open('webapp1/static/vuetify-practice/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2o2(request):
    """Vuetify練習"""
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template('vuetify-practice/data-table2.html')
    #                               ------------------------------------
    #                               1
    # 1. host1/webapp1/templates/vuetify-practice/data-table2.html を取ってきます。
    #                            ---------------------------------

    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))
