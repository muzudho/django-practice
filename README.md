# django-practice

Djangoの練習（＾～＾）  

👇 説明は Qiita に掲載（＾～＾）  

📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

# Run

```shell
cd host1

docker-compose up
```

* 起動に失敗することがある。そのときは再実行してください
* http://localhost:8000
* [Ctrl]+[C]キーで停止

URL

* auth
  * http://localhost:8000/accounts/v1/login/
  * http://localhost:8000/accounts/v1/logout/
* user
  * http://localhost:8000/practice/session-active-user-list/
  * http://localhost:8000/practice/user-list/
* http://localhost:8000/tic-tac-toe/v1o1/match-application/
* (Old) http://localhost:8000/tic-tac-toe2/
* http://localhost:8000/tic-tac-toe/v2/
* http://localhost:8000/lobby/v1/
* http://localhost:8000/admin/ - 管理画面


Product

* (Old) http://tic.warabenture.com:8000/tic-tac-toe2/
* auth
  * http://tic.warabenture.com:8000/accounts/v1/login/
  * http://tic.warabenture.com:8000/accounts/v1/logout/
* user
  * http://tic.warabenture.com:8000/practice/session-active-user-list/
  * http://tic.warabenture.com:8000/practice/user-list/
* http://tic.warabenture.com:8000/tic-tac-toe/v2/
* http://tic.warabenture.com:8000/lobby/v1/

```shell
# さくらVPSの本番環境で
cd home/ubuntu/app/host1

docker-compose up
```

モデルのマイグレーションが必要なら、  

```shell
docker-compose run --rm web python3 manage.py makemigrations webapp1

docker-compose run --rm web python manage.py migrate
```

# Others

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

# Other documents

📖 [ゼロからリアルタイムサーバーを作るまで](https://logmi.jp/tech/articles/322569)  
📖 [Pub/Subメッセージングモデルの業務利用における難しさ](https://qiita.com/TakaakiOtomo/items/badba239ade07c4ea59f)  

* セッション

📖 [Django Channelsで実装した認証付きWebsocketにPythonで接続する](https://www.denzow.me/entry/2018/07/06/003238)  

## デコレーター

📖 [【Python】初心者向けにデコレータの解説](https://djangobrothers.com/blogs/python_decorator/)  
