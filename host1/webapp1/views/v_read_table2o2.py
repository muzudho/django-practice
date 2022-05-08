from django.http import HttpResponse
from django.template import loader


def readDataTable2o2(request):
    """（追加）Vuetify練習"""
    form1Textarea1 = request.POST["textarea1"]

    template = loader.get_template('vuetify2/data-table2.html')
    context = {
        'dessertsJson': form1Textarea1
    }
    return HttpResponse(template.render(context, request))
