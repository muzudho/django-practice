from django.http import HttpResponse
from django.template import loader


def render_page1(request):
    template = loader.get_template('webapp1/practice/page1.html')
    #                               ---------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/page1.html を取得
    #                            ---------------------------

    context = {}
    return HttpResponse(template.render(context, request))


def render_page2_patch1(request):
    """ページ２　パッチ１"""
    template = loader.get_template('webapp1/practice/page2_patch1.html.txt')
    #                               --------------------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/page2_patch1.html.txt を取得
    #                            --------------------------------------

    context = {}
    return HttpResponse(template.render(context, request))


def render_page2_patch2(request):
    """ページ２　パッチ２"""
    template = loader.get_template('webapp1/practice/page2_patch2.html.txt')
    #                               --------------------------------------
    #                               1
    # 1. host1/webapp1/templates/webapp1/practice/page2_patch2.html.txt を取得
    #                            --------------------------------------

    context = {}
    return HttpResponse(template.render(context, request))
