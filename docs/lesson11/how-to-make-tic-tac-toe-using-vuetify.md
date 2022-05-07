---
title: Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！ Vuetify編
tags: Django Vuetify
author: muzudho1
slide: false
---
# 目的

前の記事で、１人２役で２窓で遊ぶ 〇×ゲーム（Tic tac toe）を作った。  
これのフロントエンドを Vuetify に置き換えたい。  

# はじめに

前提知識:  

| Key                                                            | Value                                                                                                                      |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Webブラウザ越しに２人対戦できる〇×ゲームの作成方法を知っておく | 📖[Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！](https://qiita.com/muzudho1/items/3bd5e55fbea2c0598e8b) |

この記事のアーキテクチャ:  

| Key              | Value                                     |
| ---------------- | ----------------------------------------- |
| OS               | Windows10                                 |
| Container        | Docker                                    |
| Program Language | Python 3                                  |
| Web framework    | Django                                    |
| Communication    | Web socket                                |
|                  | JSON                                      |
| Frontend         | Vuetify                                   |
| Database         | Redis                                     |
| Editor           | Visual Studio Code （以下 VSCode と表記） |

この記事は Lesson01 から続いていて、順にやってこないと ソースが足りず実行できないので注意されたい。  

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
└── 📂host1
     ├── 📂data
     │　　└── 📂db
     │         └── <たくさんのもの>
     ├── 📂webapp1
     │　　├── 📂static
     │　　│    └── 📂tic-tac-toe1
     │　　│        ├── game.js
     │　　│        └── main.css
     │　　├── 📂templates
     │　　│    └── 📂tic-tac-toe1
     │　　│        ├── game.html
     │　　│        └── index.html
     │　　├── 📂tic_tac_toe1
     │　　│    └── consumer1.py
     │　　├── 📄asgi.py
     │　　├── 📄models.py
     │　　├── 📄routing1.py
     │　　├── 📄settings.py
     │　　├── 📄urls.py
     │　　└── <いろいろ>
     ├── 📄.env
     ├── 🐳docker-compose.yml
     ├── 🐳Dockerfile
     ├── 📄manage.py
     ├── 📄requirements.txt
     └── <いろいろ>
```

以下、参考にした元記事は 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

# Step 1. favicon.ico ファイルの設置

favicon.ico は、例えば 以下のサイトで作れる。作ってきてほしい。  

📖 [Favicon Generator. For real.](https://realfavicongenerator.net/)  

例えば、以下の場所に置いてほしい  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　└── 📂static
       　　      └── 🚀favicon.ico 👈
```

favicon.ico を有効にするには HTML で設定する必要があるが、まだ作成しない。以下は例。あとで全体を再掲する。  

```plaintext
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html>
    <head>
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        中略
        <title>Tic Tac Toe</title>
    </head>
    <body>
以下略
```

# Step 2. protocol_messages.js ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　└── 📂static
       　　      ├── 📂tic-tac-toe2
       　　      │    └── protocol_messages.js 👈
       　　      └── 🚀favicon.ico
```

```js
/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class ProtocolMessages {

    /**
     * どちらかのプレイヤーが石を置いたとき
     * @param {*} sq - 升番号
     * @param {*} myPiece - X か O
     * @returns メッセージ
     */
    createDoMove(sq, myPiece) {
        return {
            "event": "CtoS_Move",
            "sq": sq,
            "myPiece": myPiece,
        }
    }

    /**
     * 引き分けたとき
     * @returns メッセージ
     */
    createDraw() {
        return {
            "event": "CtoS_End",
            "winner": PC_EMPTY_LABEL,
        }
    }

    /**
     * 対局を開始したとき
     * @returns メッセージ
     */
    createStart() {
        return {
            "event": "CtoS_Start",
        }
    }

    /**
     * どちらかのプレイヤーが勝ったとき
     * @param {*} myPiece - X か O
     * @returns メッセージ
     */
    createWon(myPiece) {
        return {
            "event": "CtoS_End",
            "winner": myPiece,
        }
    }
}
```

# Step 3. connection.js ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　└── 📂static
       　　      ├── 📂tic-tac-toe2
       　　      │    ├── connection.js 👈
       　　      │    └── protocol_messages.js
       　　      └── 🚀favicon.ico
```

```js
// 参考にした記事
// -------------
// 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

/**
 * 接続
 */
class Connection {

    constructor()
    {
        // 部屋名
        this.roomName = document.forms["form1"]["room_name"].value;

        // X か O か
        this.myPiece = document.forms["form1"]["my_piece"].value;

        // 接続文字列
        this.connectionString = `ws://${window.location.host}/tic-tac-toe2/${this.roomName}/`;
        //                                                               ^
        //                      ---------------------------- -------------------------------
        //                      1                            2
        // 1. ホスト アドレス
        // 2. URLの一部
        console.log(`[Debug] Connection#constructor roomName=${this.roomName} myPiece=${this.myPiece} connectionString=${this.connectionString}`)

        // 再接続中表示フラグ
        this.isReconnectingDisplay = false
    }

    /**
     * 設定
     * 
     * @param {*} onOpenWebSocket - Webソケットを開かれたとき
     * @param {*} onCloseWebSocket - Webソケットが閉じられたとき。 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {*} setMessageFromServer - サーバーからのメッセージがセットされる関数
     */
    connect(onOpenWebSocket, onCloseWebSocket, setMessageFromServer, onWebSocketError) {
        console.log(`[Connection#connect] Start`)

        // Webソケットを生成すると、接続も行われる。再接続したいときは、再生成する
        try {
            // 接続できないと、この生成に失敗する。catch もできない
            this.webSock1 = new WebSocket(this.connectionString);

            this.webSock1.onopen = onOpenWebSocket;
            this.webSock1.onclose = onCloseWebSocket;

            // 設定: サーバーからメッセージを受信したとき
            this.webSock1.onmessage = (e) => {
                // JSON を解析、メッセージだけ抽出
                let data1 = JSON.parse(e.data);
                let message = data1["message"];
                setMessageFromServer(message)
            };

            // this.webSock1.onerror = onWebSocketError;
            this.webSock1.addEventListener('error', (event1) => {
                onWebSocketError(event1)
            })

            // 状態を表示
            if (this.webSock1.readyState == WebSocket.CONNECTING) {
                // 未接続
                console.log('[Connect] Connecting socket.');
            } else if (this.webSock1.readyState == WebSocket.OPEN) {
                console.log('[Connect] Open socket.');
                this.webSock1.onopen();
            } else if (this.webSock1.readyState == WebSocket.CLOSING) {
                console.log('[Connect] Closing socket.');
            } else if (this.webSock1.readyState == WebSocket.CLOSED) {
                // サーバーが落ちたりしたときは、ここ
                console.log('[Connect] Closed socket.');
            } else {
                console.log(`[Connect] webSock1.readyState=${this.webSock1.readyState}`);
            }

        } catch (error) {
            // キャッチで捕まえられない
            console.log(`[Connect] Exception ${error}`);
        }

    }
}
```

# Step 4. game.js ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　└── 📂static
       　　      ├── 📂tic-tac-toe2
       　　      │    ├── connection.js
       　　      │    ├── game.js 👈
       　　      │    └── protocol_messages.js
       　　      └── 🚀favicon.ico
```

```js
/**
 * PC は Piece （駒、石、などの意味）の略です。
 * @type {number}
 */
const PC_EMPTY = 0 // Pieceがないことを表します
const PC_X = 1
const PC_O = 2

/**
 * ラベル
 * @type {string}
 */
const PC_EMPTY_LABEL = ""
const PC_X_LABEL = "X"
const PC_O_LABEL = "O"

/**
 * 盤上の升の数
 * @type {number}
 */
const BOARD_AREA = 9

/**
 * SQ is square
 * +---------+
 * | 0  1  2 |
 * | 3  4  5 |
 * | 6  7  8 |
 * +---------+
 * @type {number}
 */
const SQ_0 = 0
const SQ_1 = 1
const SQ_2 = 2
const SQ_3 = 3
const SQ_4 = 4
const SQ_5 = 5
const SQ_6 = 6
const SQ_7 = 7
const SQ_8 = 8

/**
 * 石が３つ並んでいるパターン
 */
WIN_PATTERN = [
    // +---------+
    // | *  *  * |
    // | .  .  . |
    // | .  .  . |
    // +---------+
    [SQ_0, SQ_1, SQ_2],
    // +---------+
    // | .  .  . |
    // | *  *  * |
    // | .  .  . |
    // +---------+
    [SQ_3, SQ_4, SQ_5],
    // +---------+
    // | .  .  . |
    // | .  .  . |
    // | *  *  * |
    // +---------+
    [SQ_6, SQ_7, SQ_8],
    // +---------+
    // | *  .  . |
    // | *  .  . |
    // | *  .  . |
    // +---------+
    [SQ_0, SQ_3, SQ_6],
    // +---------+
    // | .  *  . |
    // | .  *  . |
    // | .  *  . |
    // +---------+
    [SQ_1, SQ_4, SQ_7],
    // +---------+
    // | .  .  * |
    // | .  .  * |
    // | .  .  * |
    // +---------+
    [SQ_2, SQ_5, SQ_8],
    // +---------+
    // | *  .  . |
    // | .  *  . |
    // | .  .  * |
    // +---------+
    [SQ_0, SQ_4, SQ_8],
    // +---------+
    // | .  .  * |
    // | .  *  . |
    // | *  .  . |
    // +---------+
    [SQ_2, SQ_4, SQ_6]
]

/**
 * ゲーム
 */
class Game {
    constructor() {
        this.clear()

        // イベントリスナー
        this._onDoMove = () => {}
        this._onWon = () => {}
        this._onDraw = () => {}
    }

    /**
     * 石を置いたとき
     */
    set onDoMove(func) {
        this._onDoMove = func
    }

    /**
     * 勝ったとき
     */
    set onWon(func) {
        this._onWon = func
    }

    /**
     * 引き分けたとき
     */
    set onDraw(func) {
        this._onDraw = func
    }

    /**
     * クリアー
     */
    clear() {
        // 盤面
        this.board = [
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
        ];

        // 何手目
        this.countOfMove = 0;

        // 自分の手番ではない
        this.isMyTurn = false;

        // 相手の手番に着手しないでください
        this.isWaitForOther = false;
    }

    /**
     * 初期化
     */
    init(myPiece) {
        this.clear()

        // 自分の手番か
        {
            let isMyTurn;
            if (myPiece == PC_X_LABEL) {
                isMyTurn = true;
            } else {
                isMyTurn = false;
            }
            this.isMyTurn = isMyTurn;
        }

        // イベントハンドラはそのまま
    }

    /**
     * 石を置きます
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} myPiece - X か O
     * @returns 石を置けたら真、それ以外は偽
     */
    makeMove(sq, myPiece){

        if (this.board[sq] == PC_EMPTY) {
            // 空升なら

            this.countOfMove++; // 何手目を＋１

            // 石を置きます
            switch (myPiece) {
                case 'X':
                    this.board[sq] = PC_X;
                    break;
                case 'O':
                    this.board[sq] = PC_O;
                    break;
                default:
                    alert(`[Error] Invalid my piece = ${myPiece}`);
                    return false;
            }

            this._onDoMove(sq, myPiece)
        }

        // ボタンのラベルを更新
        vue1.setLabelOfButton(sq, myPiece);

        if(this.isMyTurn){
            // 終局判定
            const gameOver = this.isGameOver();

            // 打った後、負けと判定されたなら、相手が負け
            if (gameOver) {
                this._onWon(myPiece)
            }
            // 盤が埋まったら引き分け
            else if (!gameOver && this.countOfMove == 9) {
                this._onDraw()
            }
        }

        return true
    }

    /**
     * 手番を持っている方が勝っているか？
     * @returns 勝ちなら真、それ以外は偽
     */
    isGameOver(){
        if (5 <= this.countOfMove) {
            for (let squaresOfWinPattern of WIN_PATTERN) {
                if (this.isPieceInLine(squaresOfWinPattern)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * 石が３つ並んでいるか？
     * @param {*} squaresOfWinPattern - 勝ちパターン
     * @returns 並んでいれば真、それ以外は偽
     */
    isPieceInLine(squaresOfWinPattern) {
        return this.board[squaresOfWinPattern[0]] !== PC_EMPTY &&
            this.board[squaresOfWinPattern[0]] === this.board[squaresOfWinPattern[1]] &&
            this.board[squaresOfWinPattern[0]] === this.board[squaresOfWinPattern[2]];
    }
}
```

# Step 5. engine.js ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　└── 📂static
       　　      ├── 📂tic-tac-toe2
       　　      │    ├── connection.js
       　　      │    ├── engine.js 👈
       　　      │    ├── game.js
       　　      │    └── protocol_messages.js
       　　      └── 🚀favicon.ico
```

```js
/**
 * ゲームエンジン
 */
class Engine {
    /**
     * 生成
     * @param {*} onSetMessageFromServer - サーバーからのメッセージをセットする関数
     * @param {*} reconnect - 再接続ラムダ関数
     */
    constructor(onSetMessageFromServer, reconnect) {
        this._onSetMessageFromServer = onSetMessageFromServer
        this._reconnect = reconnect

        // 接続
        this._connection = new Connection();
        // メッセージ一覧
        this._protocolMessages = new ProtocolMessages();
        // ゲーム
        this._game = new Game();

        // １手進めたとき
        this._game.onDoMove = (sq, myPiece) => {
            let response = this.protocolMessages.createDoMove(sq, myPiece)
            this._connection.webSock1.send(JSON.stringify(response))
        }

        // どちらかが勝ったとき
        this._game.onWon = (myPiece) => {
            let response = this.protocolMessages.createWon(myPiece)
            this._connection.webSock1.send(JSON.stringify(response))
        }

        // 引き分けたとき
        this._game.onDraw = () => {
            let response = this.protocolMessages.createDraw()
            this._connection.webSock1.send(JSON.stringify(response))
        }

        this.connect()
    }

    /**
     * 接続
     */
    get connection() {
        return this._connection
    }

    /**
     * メッセージ一覧
     */
    get protocolMessages() {
        return this._protocolMessages
    }

    /**
     * ゲーム
     */
    get game() {
        return this._game
    }

    /**
     * 接続
     */
    connect() {
        this._connection.connect(
            // Webソケットを開かれたとき
            () => {
                console.log('WebSockets connection created.');
                let response = this.protocolMessages.createStart()
                this._connection.webSock1.send(JSON.stringify(response))
            },
            // Webソケットが閉じられたとき
            (e) => {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`);
                // 1回だけ再接続を試みます
                this._reconnect()
            },
            // サーバーからのメッセージを受信したとき
            this._onSetMessageFromServer,
            // エラー時
            (e) => {
                console.log(`Socket is error. ${e.reason}`);
            }
        )
    }
}
```

# Step 6. protocol_main.js ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　└── 📂static
       　　      ├── 📂tic-tac-toe2
       　　      │    ├── connection.js
       　　      │    ├── engine.js
       　　      │    ├── game.js
       　　      │    ├── protocol_main.js 👈
       　　      │    └── protocol_messages.js
       　　      └── 🚀favicon.ico
```

```js
/**
 * サーバーからのメッセージをセットする関数を返します
 * @returns 関数
 */
function createSetMessageFromServer() {
    return (message) => {
        // イベント
        let event = message["event"];
        // テキスト
        let text = message["text"];
        // 升番号
        let sq = message["sq"];
        // X か O
        let myPiece = message["myPiece"];
        // 勝者
        let winner = message["winner"];
        console.log(`[setMessage] event=${event} text=${text} sq=${sq} myPiece=${myPiece} winner=${winner}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "StoC_Start":
                // 対局開始の一斉通知
                vue1.init();   // 画面を初期化
                break;

            case "StoC_End":
                // 対局終了の一斉通知
                let result;
                if (winner == PC_EMPTY_LABEL) {
                    result = RESULT_DRAW
                } else if (winner == vue1.engine.connection.myPiece) {
                    result = RESULT_WON
                } else {
                    result = RESULT_LOST
                }

                vue1.setGameIsOver(result);
                break;

            case "StoC_Move":
                // 指し手の一斉通知
                if (myPiece != vue1.engine.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    vue1.engine.game.makeMove(parseInt(sq), myPiece);
                    // 自分の手番に変更
                    vue1.engine.game.isMyTurn = true;
                    vue1.engine.game.isWaitForOther = false;
                }
                break;

            default:
                console.log("No event");
        }
    };
}
```

# Step 7. index.html ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　└── 📂templates
       　　      └── 📂tic-tac-toe2
       　　            └── index.html 👈
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html>
    <head>
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" />
        <title>Tic Tac Toe</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container fluid>
                        <h1>Welcome to Tic Tac Toe Game</h1>
                        <v-form method="POST">
                            {% csrf_token %}

                            <v-text-field v-model="room.title" :rules="room.rules" counter="25" hint="a-z, A-Z, _. Max 25 characters" label="Room name" name="room_name"></v-text-field>

                            <v-select name="my_piece" v-model="selectedMyPiece" :items="pieces" item-text="selectedMyPiece" item-value="selectedMyPiece" label="Your piece" persistent-hint return-object single-line></v-select>

                            <v-btn block elevation="2" type="submit"> Start Game </v-btn>
                        </v-form>
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
                data: {
                    room: {
                        title: "Elephant",
                        rules: [(v) => v.length <= 25 || "Max 25 characters"],
                        wordsRules: [(v) => v.trim().split(" ").length <= 5 || "Max 5 words"],
                    },
                    selectedMyPiece: "X",
                    pieces: ["X", "O"],
                },
            });
        </script>
    </body>
</html>
```

# Step 8. game.html ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　└── 📂templates
       　　      └── 📂tic-tac-toe2
       　　            ├── index.html
       　　            └── game.html 👈
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html>
    <head>
        <link rel="shortcut icon" type="image/png" href="{% static 'favicon.ico' %}" />
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/@mdi/font@6.x/css/materialdesignicons.min.css" rel="stylesheet" />
        <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui" />
        <title>Tic Tac Toe</title>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container>
                        <h1>TIC TAC TOE</h1>
                        <h3>Welcome to room_{{room_name}}</h3>
                    </v-container>

                    <form name="form1" method="POST">
                        {% csrf_token %}
                        <v-container>
                            <v-row justify="center" dense>
                                <v-col>
                                    {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %} {% verbatim %}
                                    <v-btn id="square0" v-on:click="clickSquare(0)">{{label0}}</v-btn>
                                    <v-btn id="square1" v-on:click="clickSquare(1)">{{label1}}</v-btn>
                                    <v-btn id="square2" v-on:click="clickSquare(2)">{{label2}}</v-btn>
                                    {% endverbatim %}
                                </v-col>
                            </v-row>
                            <v-row justify="center" dense>
                                <v-col>
                                    {% verbatim %}
                                    <v-btn id="square3" v-on:click="clickSquare(3)">{{label3}}</v-btn>
                                    <v-btn id="square4" v-on:click="clickSquare(4)">{{label4}}</v-btn>
                                    <v-btn id="square5" v-on:click="clickSquare(5)">{{label5}}</v-btn>
                                    {% endverbatim %}
                                </v-col>
                            </v-row>
                            <v-row justify="center" dense>
                                <v-col>
                                    {% verbatim %}
                                    <v-btn id="square6" v-on:click="clickSquare(6)">{{label6}}</v-btn>
                                    <v-btn id="square7" v-on:click="clickSquare(7)">{{label7}}</v-btn>
                                    <v-btn id="square8" v-on:click="clickSquare(8)">{{label8}}</v-btn>
                                    {% endverbatim %}
                                </v-col>
                            </v-row>
                        </v-container>
                        <input type="hidden" name="room_name" value="{{room_name}}" />
                        <input type="hidden" name="my_piece" value="{{my_piece}}" />
                    </form>
                    <v-container>
                        <v-btn block elevation="2" v-on:click="clickPlayAgain()" :disabled="isDisabledPlayAgainButton()"> Play again </v-btn>
                    </v-container>
                    <v-container>
                        <v-alert type="info" color="green" v-show="isAlertYourMoveShow()">Your turn. Place your move <strong>{{my_piece}}</strong></v-alert>
                        <v-alert type="warning" color="orange" v-show="isAlertWaitForOther()">Wait for other to place the move</v-alert>
                        {% verbatim %}
                        <v-alert type="success" color="blue" v-show="isAlertResultShow()">{{result}}</v-alert>
                        {% endverbatim %}
                        <v-alert type="warning" color="orange" v-show="isAlertReconnectingShow()">Reconnecting...</v-alert>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="{% static 'tic-tac-toe2/connection.js' %}"></script>
        <script src="{% static 'tic-tac-toe2/engine.js' %}"></script>
        <script src="{% static 'tic-tac-toe2/game.js' %}"></script>
        <script src="{% static 'tic-tac-toe2/protocol_main.js' %}"></script>
        <script src="{% static 'tic-tac-toe2/protocol_messages.js' %}"></script>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            const STATE_DURING_GAME = "DuringGame";
            const STATE_GAME_IS_OVER = "GameIsOver";

            const RESULT_WON = "Won";
            const RESULT_LOST = "Lost";
            const RESULT_DRAW = "Draw";

            /**
             * 再接続関数の作成
             * @return ラムダ関数
             */
            function packReconnect() {
                // 5秒後に1回だけ再接続にトライします。
                // そのあと接続が切れれば また再接続が呼び出されるので連続します
                return () => {
                    console.log("[Reconnect] Start...");
                    vue1.engine.connection.isReconnectingDisplay = true;

                    setTimeout(() => {
                        // このコードブロックでは、 this の指しているものが コードブロックの外側のオブジェクトではないので注意
                        console.log("[Reconnect] Try...");
                        vue1.engine.connect();

                        vue1.engine.connection.isReconnectingDisplay = false;
                        console.log("[Reconnect] End");
                    }, 5000);
                };
            }

            let vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    engine: new Engine(createSetMessageFromServer(), packReconnect()),
                    state: STATE_DURING_GAME,
                    result: "",
                    label0: PC_EMPTY_LABEL,
                    label1: PC_EMPTY_LABEL,
                    label2: PC_EMPTY_LABEL,
                    label3: PC_EMPTY_LABEL,
                    label4: PC_EMPTY_LABEL,
                    label5: PC_EMPTY_LABEL,
                    label6: PC_EMPTY_LABEL,
                    label7: PC_EMPTY_LABEL,
                    label8: PC_EMPTY_LABEL,
                },
                // page loaded
                mounted: () => {
                    // ここで Vue の準備完了後の処理ができる。
                    // ただし、まだ this は初期化されてない
                },
                methods: {
                    // 画面を初期化
                    init() {
                        // console.log("[Debug] Vue#init()");
                        this.setState(STATE_DURING_GAME);

                        this.engine.game.init(this.engine.connection.myPiece);

                        // ボタンのラベルをクリアー
                        for (let sq = 0; sq < BOARD_AREA; sq += 1) {
                            this.setLabelOfButton(sq, PC_EMPTY_LABEL);
                        }
                    },
                    /**
                     * 升ボタンをクリックしたとき
                     * @param {*} sq - Square; 0 <= sq
                     */
                    clickSquare(sq) {
                        // console.log(`[Debug] Vue#clickSquare sq=${sq}`);
                        if (this.engine.game.board[sq] == PC_EMPTY) {
                            if (!this.engine.game.isMyTurn) {
                                // Wait for other to place the move
                                console.log("Wait for other to place the move");
                                this.engine.game.isWaitForOther = true;
                            } else {
                                this.engine.game.isMyTurn = false;

                                this.engine.game.makeMove(parseInt(sq), this.engine.connection.myPiece);
                            }
                        }
                    },
                    /**
                     * 升ボタンのラベル変更
                     * @param {number} sq - Square; 0 <= sq
                     * @param {*} piece - text
                     */
                    setLabelOfButton(sq, piece) {
                        // console.log(`[Debug] Vue#setLabelOfButton sq=${sq} piece=${piece}`);
                        switch (sq) {
                            case 0:
                                this.label0 = piece;
                                break;
                            case 1:
                                this.label1 = piece;
                                break;
                            case 2:
                                this.label2 = piece;
                                break;
                            case 3:
                                this.label3 = piece;
                                break;
                            case 4:
                                this.label4 = piece;
                                break;
                            case 5:
                                this.label5 = piece;
                                break;
                            case 6:
                                this.label6 = piece;
                                break;
                            case 7:
                                this.label7 = piece;
                                break;
                            case 8:
                                this.label8 = piece;
                                break;
                            default:
                                alert(`[Error] sq=${sq}`);
                                break;
                        }
                    },
                    /**
                     *
                     */
                    clickPlayAgain() {
                        console.log(`Play Again`);
                        this.init();
                    },
                    /**
                     *
                     */
                    setState(state) {
                        this.state = state;
                    },
                    /**
                     *
                     */
                    isDisabledPlayAgainButton() {
                        switch (this.state) {
                            case STATE_GAME_IS_OVER:
                                return false; // Enable
                            default:
                                return true; // Disable
                        }
                    },
                    /**
                     * 対局は終了しました
                     */
                    setGameIsOver(result) {
                        console.log(`[setGameIsOver] result=${result}`);

                        this.setState(STATE_GAME_IS_OVER); // 画面を対局終了状態へ

                        switch (result) {
                            case RESULT_DRAW:
                                this.result = "It's a draw.";
                                break;
                            case RESULT_WON:
                                this.result = "You win!";
                                break;
                            case RESULT_LOST:
                                this.result = "You lose.";
                                break;
                            default:
                                throw `unknown result = ${result}`;
                        }
                    },
                    /**
                     * 対局中で、自分の手番ならアラートを常時表示
                     */
                    isAlertYourMoveShow() {
                        return this.state == STATE_DURING_GAME && this.engine.game.isMyTurn;
                    },
                    isAlertWaitForOther() {
                        return this.engine.game.isWaitForOther;
                    },
                    /**
                     * 対局が終了していたら、結果を常時表示
                     */
                    isAlertResultShow() {
                        return this.state == STATE_GAME_IS_OVER;
                    },
                    /**
                     * 再接続中表示中なら、アラートを常時表示
                     */
                    isAlertReconnectingShow() {
                        return this.engine.connection.isReconnectingDisplay;
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 9. protocol.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　├── 📂templates
       　　│    └── 📂tic-tac-toe2
       　　│          ├── index.html
       　　│          └── game.html
       　　└── 📂tic-tac-toe2
       　　      └── protocol.py 👈
```

```py
class Protocol():
    """サーバープロトコル"""

    def execute(self, response):
        """サーバーからクライアントへ送信するメッセージの作成"""

        event = response.get("event", None)

        if event == 'CtoS_End':
            # 対局終了時
            return {
                'type': 'send_message',
                'event': "StoC_End",
                'winner': response.get("winner", None),
            }

        elif event == 'CtoS_Move':
            # 石を置いたとき
            return {
                'type': 'send_message',
                "event": "StoC_Move",
                'sq': response.get("sq", None),
                'myPiece': response.get("myPiece", None),
            }

        elif event == 'CtoS_Start':
            # 対局開始時
            return {
                'type': 'send_message',
                'event': "StoC_Start",
            }

        raise ValueError(f"Unknown event: {event}")
```

# Step 10. consumer1.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　├── 📂templates
       　　│    └── 📂tic-tac-toe2
       　　│          ├── index.html
       　　│          └── game.html
       　　└── 📂tic-tac-toe2
       　　      ├── consumer1.py 👈
       　　      └── protocol.py
```

```py
# 参考にした記事
# -------------
# 📖[Django Channels and WebSockets](https: // blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from webapp1.tic_tac_toe2.protocol import Protocol


class TicTacToe2Consumer1(AsyncJsonWebsocketConsumer):
    #          ^

    def __init__(self):
        super().__init__()
        self.protocol = Protocol()

    async def connect(self):
        """接続"""
        print("Connect")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """切断"""
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """クライアントからのメッセージの受信"""

        print(
            f"[Debug] Consumer1#receive text_data={text_data}")  # ちゃんと動いているようなら消す

        request = json.loads(text_data)
        response = self.protocol.execute(request)

        # 部屋のメンバーに一斉送信します
        await self.channel_layer.group_send(self.room_group_name, response)

    async def send_message(self, message):
        """メッセージ送信"""
        await self.send(text_data=json.dumps({
            "message": message,
        }))
```

# Step 11. views.py ファイルの編集

以下のファイルを編集してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　├── 📂templates
       　　│    └── 📂tic-tac-toe2
       　　│          ├── index.html
       　　│          └── game.html
       　　├── 📂tic-tac-toe2
       　　│    ├── consumer1.py
       　　│    └── protocol.py
       　　└── views.py 👈
```

👇追加する部分のみ抜粋

```py
from django.shortcuts import render, redirect
from django.http import Http404

# ...中略...

#                   v
def indexOfTicTacToe2(request):
    """（追加） For Tic-tac-toe2"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe2/{room_name}/?&mypiece={myPiece}')
        #                             ^
    return render(request, "tic-tac-toe2/index.html", {})
    #                                  ^


#                      v
def playGameOfTicTacToe2(request, room_name):
    """（追加） For Tic-tac-toe2"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe2/game.html", context)
    #                                  ^
```

# Step 12. urls.py ファイルの編集

以下のファイルを編集してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　├── 📂templates
       　　│    └── 📂tic-tac-toe2
       　　│          ├── index.html
       　　│          └── game.html
       　　├── 📂tic-tac-toe2
       　　│    ├── consumer1.py
       　　│    └── protocol.py
       　　├── urls.py 👈
       　　└── views.py
```

👇追加する部分のみ抜粋

```py
from django.urls import path
from . import views

urlpatterns = [
    # ...略...

    # （追加）
    path('tic-tac-toe2/', views.indexOfTicTacToe2),
    #                ^                          ^
    #     -------------
    #     1
    # 1. URLの一部

    # （追加）
    path('tic-tac-toe2/<str:room_name>/', views.playGameOfTicTacToe2),
    #                ^                                             ^
    #     -----------------------------
    #     1
    # 1. URLの一部。<room_name> に入った文字列は room_name 変数に渡されます
]
```

# Step 13. routing1.py ファイルの編集

以下のファイルを編集してほしい。  

```plaintext
└── 📂host1
     └── 📂webapp1
       　　├── 📂static
       　　│    ├── 📂tic-tac-toe2
       　　│    │    ├── connection.js
       　　│    │    ├── engine.js
       　　│    │    ├── game.js
       　　│    │    ├── protocol_main.js
       　　│    │    └── protocol_messages.js
       　　│    └── 🚀favicon.ico
       　　├── 📂templates
       　　│    └── 📂tic-tac-toe2
       　　│          ├── index.html
       　　│          └── game.html
       　　├── 📂tic-tac-toe2
       　　│    ├── consumer1.py
       　　│    └── protocol.py
       　　├── routing1.py 👈
       　　├── urls.py
       　　└── views.py
```

👇追加する部分のみ抜粋

```py
from webapp1.tic_tac_toe2.consumer1 import TicTacToe2Consumer1  # 追加
#                       ^                           ^
#    ------- ------------ ---------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

# ...中略...

websocket_urlpatterns = [

    # ...中略...

    # （追加） For Tic-tac-toe2
    url(r'^tic-tac-toe2/(?P<room_name>\w+)/$', TicTacToe2Consumer1.as_asgi()),
    #                 ^                                 ^
    #     ----------------------------------
    #     1
    # 1. URLの一部（正規表現）の Django での書き方
]
```

# Step 14. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください。  

📖 [http://localhost:8000/tic-tac-toe2/](http://localhost:8000/tic-tac-toe2/)  

# 次の記事

* 📖 [Django さくらVPS 備忘録](https://qiita.com/muzudho1/items/1d3b4b5608716463184c)

# 参考にした記事

📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  
