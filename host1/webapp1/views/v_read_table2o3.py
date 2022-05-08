import json
from django.http import JsonResponse
from webapp1.models.m_dessert import Dessert
#    ------- ------ ---------        -------
#    1       2      3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


def readDataTable2o3(request):
    """（追加）"""
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
