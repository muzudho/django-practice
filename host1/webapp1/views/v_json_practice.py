
import json
from django.http import JsonResponse


def readJsonResponse1(request):
    """JSONでの応答練習"""
    with open('webapp1/static/vuetify-practice/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    return JsonResponse(doc)
