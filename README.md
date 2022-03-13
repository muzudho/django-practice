# django-practice

Djangoの練習（＾～＾）

# Test

```shell
python -V
Python 3.9.10

docker --version
Docker version 20.10.10, build b485636

docker-compose -version
docker-compose version 1.29.2, build 5becea4c

# pip を最新に
python -m pip install --upgrade pip
```

# プロジェクトの作成

```plain
host1/
    |
    +-- docker-compose.yml
    +-- Dockerfile
    +-- requirements.txt
```

```shell
cd host1

# もう run しました。また run するなら、下図の <New> のファイルを消してください。 分かるなら、関連するDockerコンテナや、Dockerイメージも消してください
# docker-compose run web django-admin.py startproject webapp1 .
```

```plain
host1/
    |
    +-- data                <New>
            |
            +-- db          <New>
                |
                +-- たくさん <New>
    +-- webapp1/            <New>
            |
            +-- __init__.py <New>
            +-- asgi.py     <New>
            +-- settings.py <New> https://docs.docker.com/samples/django/ 見てデータベースの設定を行った
            +-- urls.py     <New>
            +-- wsgi.py     <New>
    +-- docker-compose.yml
    +-- Dockerfile
    +-- manage.py           <New>
    +-- requirements.txt
```

```shell
# docker-compose up する前に、 settings.py のデータベース設定を変えてください
docker-compose up
```

* http://localhost:8000
* [Ctrl]+[C]キーで停止


別ターミナルから:  

```shell
# コンテナに入れることの確認だけ
docker container exec -it host1_db_1 bash
#                         ----------
#                         CONTAINER NAME

cd /var/lib/postgresql/data
ls -la

exit
```

# Documents

📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  
