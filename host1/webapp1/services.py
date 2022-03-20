# from django.contrib.auth.admin import User
from django.contrib.auth.models import User
from django_grpc_framework import generics
from webapp1.serializers import UserProtoSerializer
#    -------
#    1
# 1. アプリケーション フォルダー名


class UserService(generics.ModelService):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserProtoSerializer
