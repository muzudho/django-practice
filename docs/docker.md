# Dockerコマンド備忘録

📖 [Reference documentation](https://docs.docker.com/reference/)  

```shell
docker --help
docker image --help
docker system --help

# 使ってないデータの削除
docker system prune

# Dockerイメージのリスト
docker image --help
REPOSITORY                               TAG       IMAGE ID       CREATED          SIZE
host1_web                                latest    b896a0f9e5f4   5 minutes ago    955MB

# Dockerイメージの削除
docker image rm {REPOSITORY}

# コンテナー一覧
docker ps
CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS          PORTS      NAMES
351d940bd285   postgres   "docker-entrypoint.s…"   17 minutes ago   Up 17 minutes   5432/tcp   host1_db_1

# コンテナー停止
docker stop {CONTAINER ID}

# コンテナー削除
docker rm {CONTAINER ID}
```
