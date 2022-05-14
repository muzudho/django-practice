from django.http import HttpResponse


def index(request):
    # return HttpResponse("Hello, world. You're at the webapp1 index.")
    return HttpResponse("""
<html>
<head>
    
</head>
</html>Hello, world. You're at the webapp1 index.
""")
