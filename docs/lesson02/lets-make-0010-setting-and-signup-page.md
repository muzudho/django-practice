# 目的

会員制サイトを作りたい  

1. ユーザー登録（サインアップ）
2. ログイン（サインイン）
3. 指定のメールアドレスへパスワードの変更画面URLを送る機能

を付ける方法を説明する  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Auth      | allauth                                   |
| SMTP      | smtp.gmail.com                            |
| Editor    | Visual Studio Code （以下 VSCode と表記） |
| Database  | PostgreSQL                                |

ディレクトリ構成を抜粋すると 以下のようになっている  

```plaintext
    └── 📂host1                   # あなたの開発用ディレクトリー。任意の名前
        ├── 📂data
        │   └── 📂db
        │       └── <たくさんのもの>
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📄__init__.py
        │   └── 📄urls.py
        ├── 📄asgi.py
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        ├── 📄urls.py
        └── 📄wsgi.py
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```


# 次の記事

📖 [Djangoでサインイン（利用開始）のページを作ろう！](https://qiita.com/muzudho1/items/1d34d64562ff07f1742a)  
