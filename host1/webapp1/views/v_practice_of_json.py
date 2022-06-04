
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader

from webapp1.models.m_dessert import Dessert
#    ------- ------ ---------        -------
#    1       2      3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def readJsonResponse1(request):
    """JSONでの応答練習"""
    with open('webapp1/static/webapp1/practice/vuetify-desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    return JsonResponse(doc)


def readJsonTextarea2(request):
    """JSONでの応答練習"""
    template = loader.get_template('practice/json-textarea2.html')
    #                               ----------------------------
    #                               1
    # 1. host1/webapp1/templates/practice/json-textarea2.html を取ってきます。
    #                            ----------------------------

    with open('webapp1/static/practice/webapp1/vuetify-desserts-placeholder.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    context = {
        'dessertsJson': json.dumps(doc)
    }
    return HttpResponse(template.render(context, request))


def readDataTable2o3(request):
    """JSONでの応答練習"""
    form1Textarea1 = request.POST["textarea1"]
    doc = json.loads(form1Textarea1)  # Dessert

    record = Dessert(
        name=doc["name"],
        calories=doc["calories"],
        fat=doc["fat"],
        carbs=doc["carbs"],
        protein=doc["protein"],
        iron=doc["iron"])
    record.save()

    doc2 = {
        'result': "Success"
    }
    return JsonResponse(doc2)
