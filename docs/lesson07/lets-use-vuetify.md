---
title: DjangoでフロントサイドにVuetifyを使おう！
tags: Django Docker Vuetify
author: muzudho1
slide: false
---
# 目的

Django に最初から入っている HTMLレンダラー に満足できない。  
見た目を今風にしたい。  
そこでフロントサイドに Vuetify を使う。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                                                                     | Value                                                                                                                  |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1. モデルのインスタンスの一覧表示方法を知っておく                       | 📖[Djangoでモデルのインスタンスの一覧表示をしよう！](https://qiita.com/muzudho1/items/77668130b6d941596327)             |
| 2. モデルのインスタンスの読取ページの作成方法を知っておく               | 📖[Djangoでモデルのインスタンスの読取ページを作成しよう！](https://qiita.com/muzudho1/items/ae362f53a670e265a7e4)       |
| 3. Djangoでモデルのインスタンスの削除ページの作成方法を知っておく       | 📖[Djangoでモデルのインスタンスの削除ページを作成しよう！](https://qiita.com/muzudho1/items/32694c883331c75ef059)       |
| 4. Djangoでモデルのインスタンスの作成／更新ページの作成方法を知っておく | 📖[Djangoでモデルのインスタンスの作成／更新ページを作成しよう！](https://qiita.com/muzudho1/items/806ecdba1654ae169f37) |

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
| Frontside | Vuetify                                   |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
📂host1
　├── 📂data
　│　　└── 📂db
　│　　　　└── <たくさんのもの>
　├── 📂webapp1
　│　　├── 📂templates
　│　　│    ├── 📂members
　│　　│    |   ├── 📄delete.html
　│　　│    |   ├── 📄list.html
　│　　│    |   ├── 📄read.html
　│　　│    │   └── 📄upsert.html
　│　　│    └── 📂webapp1
　│　　│        └── 📄<いろいろ>.html
　│　　├── 📄admin.py
　│　　├── 📄models.py
　│　　├── 📄settings.py
　│　　├── 📄urls.py
　│　　├── 📄views.py
　│　　└── <いろいろ>
　├── 📄.env
　├── 🐳docker-compose.yml
　├── 🐳Dockerfile
　├── 📄manage.py
　└── <いろいろ>
```

# Step 1. HTMLファイルの作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/vuetify2/hello1.html`:  

```html
<!DOCTYPE html>
<!-- See also: https://vuetifyjs.com/en/getting-started/installation/#usage-with-cdn -->
<html>
    <head>
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" />
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <v-alert type="success">This is a sample.</v-alert>
                        Hello world
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            new Vue({
                el: "#app",
                vuetify: new Vuetify(),
            });
        </script>
    </body>
</html>
```

👆 `<v-alert>` の説明は 📖[Vuetify Alerts Usage](https://vuetifyjs.com/en/components/alerts/#usage) のページにある。  

# Step 2. views.pyファイルの編集

📄`views.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/views.py`:  

```py
from django.http import HttpResponse
from django.template import loader

# Vuetify練習
def readHello(request, id=id):
    template = loader.get_template('vuetify2/hello1.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
```

# Step 3. urls.pyファイルの編集

📄`urls.py` は既存だろうから、マージしてほしい。  

📄`host1/webapp1/urls.py`:  

```py
from django.urls import path
from . import views

urlpatterns = [
    # Vuetify練習
    path('vuetify2/hello1.html', views.readHello, name='readHello'), # 追加
    #     --------------------                          ----------
    #     1                                             2
    # 1. `vuetify2/hello1.html` というURLにマッチする
    # 2. HTMLテンプレートの中で {% url 'readHello' %} のような形でURLを取得するのに使える
]
```

# Step 4. Web画面へアクセス

```shell
# （していなければ）Dockerコンテナの起動
docker-compose up
```

📖 [http://localhost:8000/vuetify2/hello1.html](http://localhost:8000/vuetify2/hello1.html)  

# 次の記事

📖 [DjangoでVuetifyのData tableを使おう！](https://qiita.com/muzudho1/items/2b01d3acce5ec1b5770b)  
