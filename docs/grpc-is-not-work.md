📖 [Django gRPC Frameworkで簡単にgRPCサービスを作成](https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/9bb58886-dd2a-4e61-b6a8-e80d4d5ccc05/)  
📖 [django-grpc-framework - Quickstart](https://djangogrpcframework.readthedocs.io/en/latest/quickstart.html)  

# 目的

Webサーバーとクライアント間のアプリで通信するのにいちいちJSON書くのめんどくさい。楽したい。  
だから **gRPC** を使う。  
いきなり使うのは難しいので、サンプルプログラムで説明する。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                                                           | Value                                                                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| WebページへJSON形式のテキストを渡す方法を知っておく           | 📖[DjangoのWebページへJSON形式のテキストを渡そう！](https://qiita.com/muzudho1/items/c50859d9bde800d06a62)           |
| Webサーバーとクライアント側のアプリで通信する方法を知っておく | 📖[DjangoのWebサーバーとクライアント側のアプリで通信しよう！](https://qiita.com/muzudho1/items/9bad88a4092bf83a0f12) |

この記事のアーキテクチャ:  

| Key           | Value                                     |
| ------------- | ----------------------------------------- |
| OS            | Windows10                                 |
| Container     | Docker                                    |
| Web framework | Django                                    |
| Communication | gRPC                                      |
| Editor        | Visual Studio Code （以下 VSCode と表記） |

一番参考になる元記事は 📖[Django gRPC Frameworkで簡単にgRPCサービスを作成](https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/05f253f8-c11b-4c91-8091-989eb2600a7b/9bb58886-dd2a-4e61-b6a8-e80d4d5ccc05/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
├── <いろいろ>
└── 📂host1
     ├── 📂data
     │　　└── 📂db
     │　　　　└── <たくさんのもの>
     ├── 📂webapp1
     │　　├── 📂templates
     │　　├── 📄asgi.py
     │　　├── 📄models.py
     │　　├── 📄settings.py
     │　　├── 📄urls.py
     │　　├── 📄views.py
     │　　└── <いろいろ>
     ├── 📄.env
     ├── 🐳docker-compose.yml
     ├── 🐳Dockerfile
     ├── 📄manage.py
     ├── 📄requirements.txt
     └── <いろいろ>
```

# Step 1. requirements.txt の設定

（無いものを）ファイルの末尾にでも追加してほしい。  

📄host1/requirements.txt:  

```shell
# For gRPC
# （追加済みだろ） Django>=3.0,<4.0
djangorestframework>=3.12.2
djangogrpcframework>=0.2
grpcio>=1.36.0
grpcio-tools>=1.36.0
```

# Step 2. settings.py ファイルの編集

以下のファイルは既存だろうから、マージしてほしい。  

📄host1/webapp1/settings.py:  

```py
INSTALLED_APPS = [
    # ...略...

    # （追加） For gRPC
    'django_grpc_framework',
]
```

# Step 3. コマンド実行＜その１＞

以下のコマンドを打鍵してほしい。  
長いコマンドなので画面を横に伸ばしてほしい。  

```shell
docker-compose run --rm web python3 manage.py generateproto --model django.contrib.auth.models.User --fields id,username,email,groups --file account.proto
#                                             -------------         -------------------------------          ------------------------        -------------
#                                             1                     2                                        3                               4
# 1. gRPC で使うファイルを生成するためのコマンド
# 2. Django に最初から入っている User モデル
# 3. "1."の User モデルのフィールドで、アクセスしたいもの
# 4. 出力ファイル。拡張子は ".proto"
```

以下のファイルが生成される。  

```plaintext
└── 📂host1
     └── 📄account.proto
```

# Step 4. コマンド実行＜その２＞

以下のコマンドを打鍵してほしい。  
長いコマンドなので画面を横に伸ばしてほしい。  

```shell
docker-compose run --rm web python3 -m grpc_tools.protoc --proto_path=./ --python_out=./ --grpc_python_out=./ ./account.proto
#                                                                                                             ---------------
#                                                                                                             1
# 1. さきほど生成したファイル
```

以下のファイルが生成される。  

```plaintext
└── 📂host1
     ├── 📄account_pb2_grpc.py
     └── 📄account_pb2.py
```

# Step 5. serializers.py ファイルの作成

以下のファイルを作成してほしい

📄`host1/webapp1/serializers.py`:  

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

# Step 6. services.py ファイルの作成

以下のファイルを作成してほしい

📄`host1/webapp1/services.py`:  

```py
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
```

# Step 6. urls.py ファイルの編集

以下のように該当箇所を追加してほしい。  

📄host1/webapp1/urls.py:  

```py
import account_pb2_grpc                  # 追加
from webapp1.services import UserService # 追加
#    -------
#    1
# 1. アプリケーション フォルダー名

urlpatterns = [] # 変更なし


def grpc_handlers(server):  # 追加
    account_pb2_grpc.add_UserControllerServicer_to_server(
        UserService.as_servicer(), server)
```

# Step 7. grpc_client1.py ファイルの作成

以下のファイルを作成してほしい

📄`host1/grpc_client1.py`:  

```py
import grpc
import account_pb2
import account_pb2_grpc

with grpc.insecure_channel('0.0.0.0:8000') as channel:
    #                       ------- ----
    #                       1       2
    # 1. Docker を使っているときは localhost ではなく 0.0.0.0 にする
    # 2. ポート番号
    stub = account_pb2_grpc.UserControllerStub(channel)
    for user in stub.List(account_pb2.UserListRequest()):
        print(user, end='')
```

See also: 📖 ["error": "14 UNAVAILABLE: failed to connect to all addresses" c# .NET5.0 Newbie](https://groups.google.com/g/grpc-io/c/TqEjPkIIUs4?pli=1)  

# Step 8. Yaml ファイルの設定

以下のファイルの該当箇所を追記してほしい

📄host1/docker-compose.yml

```yaml
  # Djangoアプリ
  web:
    environment:
      # （追加） For gRPC Debug
      - GRPC_TRACE=all
      - GRPC_VERBOSITY=DEBUG
```

See also:
📖 [grpc method call error: Failed to pick subchannel](https://stackoverflow.com/questions/68217975/grpc-method-call-error-failed-to-pick-subchannel)  
📖 [GRPC not working. Error: Failed to connect to all addresses](https://github.com/tensorflow/serving/issues/1770)  
📖 [grpc Failed to pick subchannel](https://github.com/grpc/grpc/issues/23340)  

# Step 9. Dockerfile ファイルの設定

以下のファイルの該当箇所を追記してほしい

📄host1/Dockerfile

```Dockerfile
# 例えばファイルの上のあたりで
# （追加） For gRPC Debug
ENV http_proxy=
ENV https_proxy=
```

📖 [How do you unset an environment variable in Dockerfile?](https://dockerdevops.quora.com/How-to-unset-an-environment-variable-in-Dockerfile)  

# Step 10. コマンド実行＜その３＞

Dockerコンテナは停止しているものとし、以下のコマンドを打鍵してほしい。  

```shell
cd host1

docker-compose build
```

# Step 11. コマンド実行＜その４＞

別にターミナルを１つ開いて、以下のコマンドを打鍵してほしい。  

```shell
cd host1

docker-compose run --rm web python3 manage.py grpcrunserver --dev
```

gRPC に対応したWebサーバーが開発モードとして起動する。  

# Step 12. コマンド実行＜その５＞

"Step 8." とは別のターミナルを１つ開いて、以下のコマンドを打鍵してほしい。  

```shell
cd host1

docker-compose run --rm web python3 grpc_client1.py
```

# 参考にした記事

📖 [gRPC: 14 UNAVAILABLE: failed to connect to all addresses](https://stackoverflow.com/questions/59823424/grpc-14-unavailable-failed-to-connect-to-all-addresses)  
