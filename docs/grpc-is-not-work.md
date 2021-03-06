ð [Django gRPC Frameworkã§ç°¡åã«gRPCãµã¼ãã¹ãä½æ](https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/9bb58886-dd2a-4e61-b6a8-e80d4d5ccc05/)  
ð [django-grpc-framework - Quickstart](https://djangogrpcframework.readthedocs.io/en/latest/quickstart.html)  

# ç®ç

Webãµã¼ãã¼ã¨ã¯ã©ã¤ã¢ã³ãéã®ã¢ããªã§éä¿¡ããã®ã«ãã¡ãã¡JSONæ¸ãã®ããã©ããããæ¥½ãããã  
ã ãã **gRPC** ãä½¿ãã  
ãããªãä½¿ãã®ã¯é£ããã®ã§ããµã³ãã«ãã­ã°ã©ã ã§èª¬æããã  

# ã¯ããã«

ãã®é£è¼ã®æåã®ãã¼ã¸: ð [DjangoãDockerã³ã³ããã¸ã¤ã³ã¹ãã¼ã«ãããï¼](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

åæç¥è­:  

| Key                                                           | Value                                                                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Webãã¼ã¸ã¸JSONå½¢å¼ã®ãã­ã¹ããæ¸¡ãæ¹æ³ãç¥ã£ã¦ãã           | ð[Djangoã®Webãã¼ã¸ã¸JSONå½¢å¼ã®ãã­ã¹ããæ¸¡ããï¼](https://qiita.com/muzudho1/items/c50859d9bde800d06a62)           |
| Webãµã¼ãã¼ã¨ã¯ã©ã¤ã¢ã³ãå´ã®ã¢ããªã§éä¿¡ããæ¹æ³ãç¥ã£ã¦ãã | ð[Djangoã®Webãµã¼ãã¼ã¨ã¯ã©ã¤ã¢ã³ãå´ã®ã¢ããªã§éä¿¡ãããï¼](https://qiita.com/muzudho1/items/9bad88a4092bf83a0f12) |

ãã®è¨äºã®ã¢ã¼ã­ãã¯ãã£:  

| Key           | Value                                     |
| ------------- | ----------------------------------------- |
| OS            | Windows10                                 |
| Container     | Docker                                    |
| Web framework | Django                                    |
| Communication | gRPC                                      |
| Editor        | Visual Studio Code ï¼ä»¥ä¸ VSCode ã¨è¡¨è¨ï¼ |

ä¸çªåèã«ãªãåè¨äºã¯ ð[Django gRPC Frameworkã§ç°¡åã«gRPCãµã¼ãã¹ãä½æ](https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/9bb58886-dd2a-4e61-b6a8-e80d4d5ccc05/) ã ã  
ãããã®è¨äºã¯åã« **ãã£ã¦ã¿ã** ãããã®ä½ç½®ã¥ãã ã  

åã®è¨äºããç¶ãã¦ãã¦ããã£ã¬ã¯ããªæ§æãæç²ããã¨ ä»¥ä¸ã®ããã«ãªã£ã¦ããã  

```plaintext
âââ <ãããã>
âââ ðhost1
     âââ ðdata
     âããâââ ðdb
     âããããâââ <ããããã®ãã®>
     âââ ðwebapp1
     âããâââ ðtemplates
     âããâââ ðasgi.py
     âããâââ ðmodels.py
     âããâââ ðsettings.py
     âããâââ ðurls.py
     âããâââ ðviews.py
     âããâââ <ãããã>
     âââ ð.env
     âââ ð³docker-compose.yml
     âââ ð³Dockerfile
     âââ ðmanage.py
     âââ ðrequirements.txt
     âââ <ãããã>
```

# Step 1. requirements.txt ã®è¨­å®

ï¼ç¡ããã®ãï¼ãã¡ã¤ã«ã®æ«å°¾ã«ã§ãè¿½å ãã¦ã»ããã  

ðhost1/requirements.txt:  

```shell
# For gRPC
# ï¼è¿½å æ¸ã¿ã ãï¼ Django>=3.0,<4.0
djangorestframework>=3.12.2
djangogrpcframework>=0.2
grpcio>=1.36.0
grpcio-tools>=1.36.0
```

# Step 2. settings.py ãã¡ã¤ã«ã®ç·¨é

ä»¥ä¸ã®ãã¡ã¤ã«ã¯æ¢å­ã ããããããã¼ã¸ãã¦ã»ããã  

ðhost1/webapp1/settings.py:  

```py
INSTALLED_APPS = [
    # ...ç¥...

    # ï¼è¿½å ï¼ For gRPC
    'django_grpc_framework',
]
```

# Step 3. ã³ãã³ãå®è¡ï¼ãã®ï¼ï¼

ä»¥ä¸ã®ã³ãã³ããæéµãã¦ã»ããã  
é·ãã³ãã³ããªã®ã§ç»é¢ãæ¨ªã«ä¼¸ã°ãã¦ã»ããã  

```shell
docker-compose run --rm web python3 manage.py generateproto --model django.contrib.auth.models.User --fields id,username,email,groups --file account.proto
#                                             -------------         -------------------------------          ------------------------        -------------
#                                             1                     2                                        3                               4
# 1. gRPC ã§ä½¿ããã¡ã¤ã«ãçæããããã®ã³ãã³ã
# 2. Django ã«æåããå¥ã£ã¦ãã User ã¢ãã«
# 3. "1."ã® User ã¢ãã«ã®ãã£ã¼ã«ãã§ãã¢ã¯ã»ã¹ããããã®
# 4. åºåãã¡ã¤ã«ãæ¡å¼µå­ã¯ ".proto"
```

ä»¥ä¸ã®ãã¡ã¤ã«ãçæãããã  

```plaintext
âââ ðhost1
     âââ ðaccount.proto
```

# Step 4. ã³ãã³ãå®è¡ï¼ãã®ï¼ï¼

ä»¥ä¸ã®ã³ãã³ããæéµãã¦ã»ããã  
é·ãã³ãã³ããªã®ã§ç»é¢ãæ¨ªã«ä¼¸ã°ãã¦ã»ããã  

```shell
docker-compose run --rm web python3 -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./account.proto
#                                                                                                             ---------------
#                                                                                                             1
# 1. ããã»ã©çæãããã¡ã¤ã«
```

ä»¥ä¸ã®ãã¡ã¤ã«ãçæãããã  

```plaintext
âââ ðhost1
     âââ ðaccount_pb2_grpc.py
     âââ ðaccount_pb2.py
```

# Step 5. serializers.py ãã¡ã¤ã«ã®ä½æ

ä»¥ä¸ã®ãã¡ã¤ã«ãä½æãã¦ã»ãã

ð`host1/webapp1/serializers.py`:  

```py
# from django.contrib.auth.admin import User
from django.contrib.auth.models import User
from django_grpc_framework import proto_serializers
import account_pb2


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = User
        proto_class = account_pb2.User
        fields = ['id', 'username', 'email', 'groups']
```

# Step 6. services.py ãã¡ã¤ã«ã®ä½æ

ä»¥ä¸ã®ãã¡ã¤ã«ãä½æãã¦ã»ãã

ð`host1/webapp1/services.py`:  

```py
# from django.contrib.auth.admin import User
from django.contrib.auth.models import User
from django_grpc_framework import generics
from webapp1.serializers import UserProtoSerializer
#    -------
#    1
# 1. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å


class UserService(generics.ModelService):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserProtoSerializer
```

# Step 6. urls.py ãã¡ã¤ã«ã®ç·¨é

ä»¥ä¸ã®ããã«è©²å½ç®æãè¿½å ãã¦ã»ããã  

ðhost1/webapp1/urls.py:  

```py
import account_pb2_grpc                  # è¿½å 
from webapp1.services import UserService # è¿½å 
#    -------
#    1
# 1. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å

urlpatterns = [] # å¤æ´ãªã


def grpc_handlers(server):  # è¿½å 
    account_pb2_grpc.add_UserControllerServicer_to_server(
        UserService.as_servicer(), server)
```

# Step 7. grpc_client1.py ãã¡ã¤ã«ã®ä½æ

ä»¥ä¸ã®ãã¡ã¤ã«ãä½æãã¦ã»ãã

ð`host1/grpc_client1.py`:  

```py
import grpc
import account_pb2
import account_pb2_grpc

with grpc.insecure_channel('0.0.0.0:8000') as channel:
    #                       ------- ----
    #                       1       2
    # 1. Docker ãä½¿ã£ã¦ããã¨ãã¯ localhost ã§ã¯ãªã 0.0.0.0 ã«ãã
    # 2. ãã¼ãçªå·
    stub = account_pb2_grpc.UserControllerStub(channel)
    for user in stub.List(account_pb2.UserListRequest()):
        print(user, end='')
```

See also: ð ["error": "14 UNAVAILABLE: failed to connect to all addresses" c# .NET5.0 Newbie](https://groups.google.com/g/grpc-io/c/TqEjPkIIUs4?pli=1)  

# Step 8. Yaml ãã¡ã¤ã«ã®è¨­å®

ä»¥ä¸ã®ãã¡ã¤ã«ã®è©²å½ç®æãè¿½è¨ãã¦ã»ãã

ðhost1/docker-compose.yml

```yaml
  # Djangoã¢ããª
  web:
    environment:
      # ï¼è¿½å ï¼ For gRPC Debug
      - GRPC_TRACE=all
      - GRPC_VERBOSITY=DEBUG
```

See also:
ð [grpc method call error: Failed to pick subchannel](https://stackoverflow.com/questions/68217975/grpc-method-call-error-failed-to-pick-subchannel)  
ð [GRPC not working. Error: Failed to connect to all addresses](https://github.com/tensorflow/serving/issues/1770)  
ð [grpc Failed to pick subchannel](https://github.com/grpc/grpc/issues/23340)  

# Step 9. Dockerfile ãã¡ã¤ã«ã®è¨­å®

ä»¥ä¸ã®ãã¡ã¤ã«ã®è©²å½ç®æãè¿½è¨ãã¦ã»ãã

ðhost1/Dockerfile

```Dockerfile
# ä¾ãã°ãã¡ã¤ã«ã®ä¸ã®ãããã§
# ï¼è¿½å ï¼ For gRPC Debug
ENV http_proxy=
ENV https_proxy=
```

ð [How do you unset an environment variable in Dockerfile?](https://dockerdevops.quora.com/How-to-unset-an-environment-variable-in-Dockerfile)  

# Step 10. ã³ãã³ãå®è¡ï¼ãã®ï¼ï¼

Dockerã³ã³ããã¯åæ­¢ãã¦ãããã®ã¨ããä»¥ä¸ã®ã³ãã³ããæéµãã¦ã»ããã  

```shell
cd host1

docker-compose build
```

# Step 11. ã³ãã³ãå®è¡ï¼ãã®ï¼ï¼

å¥ã«ã¿ã¼ããã«ãï¼ã¤éãã¦ãä»¥ä¸ã®ã³ãã³ããæéµãã¦ã»ããã  

```shell
cd host1

docker-compose run --rm web python3 manage.py grpcrunserver --dev
```

gRPC ã«å¯¾å¿ããWebãµã¼ãã¼ãéçºã¢ã¼ãã¨ãã¦èµ·åããã  

# Step 12. ã³ãã³ãå®è¡ï¼ãã®ï¼ï¼

"Step 8." ã¨ã¯å¥ã®ã¿ã¼ããã«ãï¼ã¤éãã¦ãä»¥ä¸ã®ã³ãã³ããæéµãã¦ã»ããã  

```shell
cd host1

docker-compose run --rm web python3 grpc_client1.py
```

# åèã«ããè¨äº

ð [gRPC: 14 UNAVAILABLE: failed to connect to all addresses](https://stackoverflow.com/questions/59823424/grpc-14-unavailable-failed-to-connect-to-all-addresses)  
