from django.http import HttpResponse
from django.template import loader


def render_index(request):
    template = loader.get_template('webapp1/index.html')
    #                               ------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/index.html を取得
    #                            ------------------

    context = {}
    return HttpResponse(template.render(context, request))

    # HTML をハードコーディングすることもできる
    # return HttpResponse("""Hello, world. You're at the webapp1 index.<br/>
    #                    <a href="home/v1/">ホーム</a>""")
