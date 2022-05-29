from django.http import HttpResponse


def index(request):
    return HttpResponse("""Hello, world. You're at the webapp1 index.<br/>
                        <a href="home/v1/">ホーム</a>""")
