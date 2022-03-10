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

# もう run しました
# docker-compose run web django-admin.py startproject webapp1 .
```

```plain
host1/
    |
    +-- webapp1/            <New>
            |
            +-- __init__.py <New>
            +-- asgi.py     <New>
            +-- settings.py <New>
            +-- urls.py     <New>
            +-- wsgi.py     <New>
    +-- docker-compose.yml
    +-- Dockerfile
    +-- manage.py <New>
    +-- requirements.txt
```
