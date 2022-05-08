import json
from django.http import JsonResponse


def readJsonResponse1(request):
    """（追加）JSONでの応答練習"""
    with open('webapp1/static/desserts.json', mode='r', encoding='utf-8') as f:
        doc = json.load(f)

    return JsonResponse(doc)
