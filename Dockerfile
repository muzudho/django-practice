FROM python:3

# Djangoで、出力をPythonでバッファリングせずにターミナルに直接送信します
ENV PYTHONUNBUFFERED 1

# コンテナに /code ディレクトリを作成します
RUN mkdir /code

# 以降、 /code ディレクトリで作業します
WORKDIR /code

# requirements.txtを /code/ ディレクトリへコピーします
ADD requirements.txt /code/

# requirements.txtに従ってpip installします
RUN pip install -r requirements.txt

# 開発環境のファイルを /code/ へコピーします
ADD . /code/
