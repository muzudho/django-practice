# django-practice

Djangoの練習（＾～＾）  

👇 説明は Qiita に掲載（＾～＾）  

📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

# Run

```shell
cd host1

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

# Other documents
