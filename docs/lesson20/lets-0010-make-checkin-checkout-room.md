# 目的

ゲーム対局部屋に入るときは Room モデルのレコードに 自分のユーザー名を上書きし、  
自分の Profile レコードの match_state フィールドを 3 （対局中）に上書きしたい  
（チェックイン）  

ゲーム対局部屋から出るときは Room モデルのレコードから 自分のユーザー名を消し、  
自分の Profile レコードの match_state フィールドを 0 （休憩中）に上書きしたい  
（チェックアウト）  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    └── 📄<いろいろ>
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂models_helper
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │   │   └── 📂practice
        │   │   │       └── 📄<いろいろ>.js
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂tic-tac-toe
        │   │       │   ├── 📂v1
        │   │       │   └── 📂v2
        │   │       │       ├── 📄match_request.html
        │   │       │       └── 📄play.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           ├── 📄consumer.py
        │   │           └── 📄protocol.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── 📄<いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── 📄<いろいろ>
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. プロトコル実装 - protocol_messages.js ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                └── 📂tic-tac-toe
                    └── 📂v3
👉                      └── protocol_messages.js
```

```js
/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class ProtocolMessagesV3 {
    /**
     * プレイヤーが部屋に入ります
     * @param {*} roomName - 部屋名
     * @param {*} myPiece - X か O
     * @param {*} userId - ユーザーId
     * @returns メッセージ
     */
    checkin(roomName, myPiece, userId) {
        return {
            event: "CtoS_Checkin",
            roomName: roomName,
            myPiece: myPiece,
            userId: userId,
        };
    }

    /**
     * プレイヤーが部屋から出ます
     * @param {*} roomName - 部屋名
     * @param {*} myPiece - X か O
     * @param {*} userId - ユーザーId
     * @returns メッセージ
     */
    checkout(roomName, myPiece, userId) {
        return {
            event: "CtoS_Checkout",
            roomName: roomName,
            myPiece: myPiece,
            userId: userId,
        };
    }
}
```
