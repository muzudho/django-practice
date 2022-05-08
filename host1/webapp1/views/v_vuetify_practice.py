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
