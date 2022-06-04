# 目的

前の記事で、１人２役で２窓で遊ぶ 〇×ゲーム（Tic tac toe）を作った。  
これのフロントエンドを Vuetify に置き換えたい  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

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

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    └── <いろいろ>
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   │       ├── 📂practice
        │   │       │   └── 📄vuetify-desserts.json
        │   │       └── 📂tic-tac-toe
        │   │           └── 📂v1
        │   │               ├── 📄game.js
        │   │               └── 📄main.css
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       ├── 📂tic-tac-toe
        │   │       │   └── 📂v1
        │   │       │       └── 📄<いろいろ>.html
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       └── 📂v1
        │   │           └── 📄consumer.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── <いろいろ>
```

以下、参考にした元記事は 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. アイコンの設定 - favicon.ico ファイル

favicon.ico は、例えば 以下のサイトで作れる。作ってきてほしい。  

📖 [Favicon Generator. For real.](https://realfavicongenerator.net/)  

例えば、以下の場所に置いてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
👉              └── 🚀favicon.ico
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

# Step 3. プロトコル実装 - protocol_messages.js ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
👉              │           └── protocol_messages.js
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

# Step 4. 通信接続の作成 - connection.js ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
👉              │           ├── connection.js
                │           └── protocol_messages.js
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
    constructor() {
        // 部屋名
        this._roomName = "";

        // X か O か
        this._myPiece = "";

        // 接続文字列（初期値はダミー文字列）
        this._connectionString = `ws://example.com/this/is/a/path/room_name/`;

        // 再接続中表示フラグ
        this.isReconnectingDisplay = false;
    }

    /**
     * X か O
     */
    get myPiece() {
        return this._myPiece;
    }

    /**
     * セットアップ
     *
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - (roomName, myPiece) return connectionString
     */
    setup(roomName, myPiece, convertPartsToConnectionString) {
        // console.log(`[Debug][Connection#setup] roomName=[${roomName}] myPiece=[${myPiece}]`);
        this._roomName = roomName;
        this._myPiece = myPiece;
        this._connectionString = convertPartsToConnectionString(this._roomName, this._myPiece);
    }

    /**
     * 設定
     *
     * @param {*} onOpenWebSocket - Webソケットを開かれたとき
     * @param {*} onCloseWebSocket - Webソケットが閉じられたとき。 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {*} setMessageFromServer - サーバーからのメッセージがセットされる関数
     */
    connect(onOpenWebSocket, onCloseWebSocket, setMessageFromServer, onWebSocketError) {
        // console.log(`[Debug][Connection#connect] Start this._connectionString=[${this._connectionString}]`);

        // Webソケットを生成すると、接続も行われる。再接続したいときは、再生成する
        try {
            // 接続できないと、この生成に失敗する。catch もできない
            this.webSock1 = new WebSocket(this._connectionString);
            // console.log(`[Debug][Connection#connect] Connecting...`);

            this.webSock1.onopen = onOpenWebSocket;
            this.webSock1.onclose = onCloseWebSocket;

            // 設定: サーバーからメッセージを受信したとき
            this.webSock1.onmessage = (e) => {
                // JSON を解析、メッセージだけ抽出
                let data1 = JSON.parse(e.data);
                let message = data1["message"];
                setMessageFromServer(message);
            };

            // this.webSock1.onerror = onWebSocketError;
            this.webSock1.addEventListener("error", (event1) => {
                onWebSocketError(event1);
            });

            // 状態を表示
            if (this.webSock1.readyState == WebSocket.CONNECTING) {
                // 未接続
                console.log("[Connect] Connecting socket.");
            } else if (this.webSock1.readyState == WebSocket.OPEN) {
                console.log("[Connect] Open socket.");
                this.webSock1.onopen();
            } else if (this.webSock1.readyState == WebSocket.CLOSING) {
                console.log("[Connect] Closing socket.");
            } else if (this.webSock1.readyState == WebSocket.CLOSED) {
                // サーバーが落ちたりしたときは、ここ
                console.log("[Connect] Closed socket.");
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

# Step 5. ゲームルール定義 - game_rule.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── connection.js
👉              │           ├── game_rule.js
                │           └── protocol_messages.js
                └── 🚀favicon.ico
```

```js
/**
 * PC は Piece （駒、石、などの意味）の略です。
 * @type {number}
 */
const PC_EMPTY = 0; // Pieceがないことを表します
const PC_X = 1;
const PC_O = 2;

/**
 * ラベル
 * @type {string}
 */
const PC_EMPTY_LABEL = "";
const PC_X_LABEL = "X";
const PC_O_LABEL = "O";

/**
 * 盤上の升の数
 * @type {number}
 */
const BOARD_AREA = 9;

/**
 * SQ is square
 * +---------+
 * | 0  1  2 |
 * | 3  4  5 |
 * | 6  7  8 |
 * +---------+
 * @type {number}
 */
const SQ_0 = 0;
const SQ_1 = 1;
const SQ_2 = 2;
const SQ_3 = 3;
const SQ_4 = 4;
const SQ_5 = 5;
const SQ_6 = 6;
const SQ_7 = 7;
const SQ_8 = 8;

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
    [SQ_2, SQ_4, SQ_6],
];
```

# Step 6. 遊具作成 - playground_equipment.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── connection.js
                │           ├── game_rule.js
👉              │           ├── playground_equipment.js
                │           └── protocol_messages.js
                └── 🚀favicon.ico
```

```js
/**
 * 遊具
 */
class PlaygroundEquipment {
    constructor() {
        this.clear();
    }

    /**
     * クリアー
     */
    clear() {
        // 盤面
        this._board = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];

        // 何手目
        this._countOfMove = 0;
    }

    /**
     * 盤上のマス番号で示して、駒を取得
     * @param {number} sq - マス番号
     */
    getPieceBySq(sq) {
        return this._board[sq];
    }

    /**
     * 盤上のマスに駒を上書きします
     *
     * @param {*} sq - マス番号
     * @param {*} piece - 駒
     */
    setPiece(sq, piece) {
        this._board[sq] = piece;
    }

    /**
     * 手数を１増やします
     */
    incrementCountOfMove() {
        this._countOfMove++;
    }

    /**
     * マスがすべて埋まっていますか
     */
    isBoardFill() {
        return this._countOfMove == 9;
    }

    /**
     * 同じ駒が３個ありますか
     */
    isThere3SamePieces() {
        return 5 <= this._countOfMove;
    }
}
```

# Step 7. ユーザーコントロール作成 - user_ctrl.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄connection.js
                │           ├── 📄game_rule.js
                │           ├── 📄protocol_messages.js
👉              │           └── 📄user_ctrl.js
                └── 🚀favicon.ico
```

```js
/**
 * ユーザーコントロール
 */
class UserCtrl {
    /**
     *
     * @param {*} playeq - 遊具
     */
    constructor(playeq) {
        // 遊具
        this._playeq = playeq;

        this.clear();

        // イベントリスナー
        this._onDoMove = () => {};
    }

    /**
     * 石を置いたとき
     */
    set onDoMove(func) {
        this._onDoMove = func;
    }

    /**
     * クリアー
     */
    clear() {
        // console.log(`[Debug][UserCtrl#clear] Begin this.isMyTurn=${this.isMyTurn}`);

        // 遊具
        this._playeq.clear();

        // 自分の手番ではない
        this.isMyTurn = false;

        // 相手の手番に着手しないでください
        this.isWaitForOther = false;

        // console.log(`[Debug][UserCtrl#clear] End this.isMyTurn=${this.isMyTurn}`);
    }

    /**
     * 初期化
     */
    init(myPiece) {
        this.clear();

        // 自分の手番か
        {
            let isMyTurn;

            // console.log(`[Debug][UserCtrl#init] myPiece=${myPiece} PC_X_LABEL=${PC_X_LABEL}`);

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
    doMove(sq, myPiece) {
        if (this._playeq.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら

            this._playeq.incrementCountOfMove(); // 手数を１増やします

            // 石を置きます
            switch (myPiece) {
                case PC_X_LABEL:
                    this._playeq.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    this._playeq.setPiece(sq, PC_O);
                    break;
                default:
                    alert(`[Error] Invalid my piece = ${myPiece}`);
                    return false;
            }

            this._onDoMove(sq, myPiece);
        }

        return true;
    }
}
```

# Step 8. 審判作成 - judge_ctrl.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄connection.js
                │           ├── 📄game_rule.js
👉              │           ├── 📄judge_ctrl.js
                │           ├── 📄protocol_messages.js
                │           └── 📄user_ctrl.js
                └── 🚀favicon.ico
```

```js
/**
 * 審判コントロール
 */
class JudgeCtrl {
    /**
     *
     * @param {*} playeq - 遊具
     * @param {*} userCtrl - ユーザーコントロール
     */
    constructor(playeq, userCtrl) {
        // 遊具
        this._playeq = playeq;

        // ユーザーコントロール
        this._userCtrl = userCtrl;

        // イベントリスナー
        this._onWon = () => {};
        this._onDraw = () => {};
    }

    /**
     * 勝ったとき
     */
    set onWon(func) {
        this._onWon = func;
    }

    /**
     * 引き分けたとき
     */
    set onDraw(func) {
        this._onDraw = func;
    }

    /**
     * 勝敗判定
     */
    doJudge(myPiece) {
        if (this._userCtrl.isMyTurn) {
            // 終局判定
            const gameOver = this.#isGameOver();

            // 打った後、負けと判定されたなら、相手が負け
            if (gameOver) {
                this._onWon(myPiece);
            }
            // 盤が埋まったら引き分け
            else if (!gameOver && this._playeq.isBoardFill()) {
                this._onDraw();
            }
        }
    }

    /**
     * 手番を持っている方が勝っているか？
     * @returns 勝ちなら真、それ以外は偽
     */
    #isGameOver() {
        if (this._playeq.isThere3SamePieces()) {
            for (let squaresOfWinPattern of WIN_PATTERN) {
                if (this.#isPieceInLine(squaresOfWinPattern)) {
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
    #isPieceInLine(squaresOfWinPattern) {
        return (
            this._playeq.getPieceBySq(squaresOfWinPattern[0]) !== PC_EMPTY && //
            this._playeq.getPieceBySq(squaresOfWinPattern[0]) === this._playeq.getPieceBySq(squaresOfWinPattern[1]) &&
            this._playeq.getPieceBySq(squaresOfWinPattern[0]) === this._playeq.getPieceBySq(squaresOfWinPattern[2])
        );
    }
}
```

# Step 9. ゲームエンジン作成 - engine.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄connection.js
👉              │           ├── 📄engine.js
                │           ├── 📄game_rule.js
                │           ├── 📄judge_ctrl.js
                │           ├── 📄protocol_messages.js
                │           └── 📄user_ctrl.js
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
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
     */
    constructor(onSetMessageFromServer, reconnect, roomName, myPiece, convertPartsToConnectionString) {
        this._onSetMessageFromServer = onSetMessageFromServer;
        this._reconnect = reconnect;

        // 接続
        this._connection = new Connection();
        this._connection.setup(roomName, myPiece, convertPartsToConnectionString);

        // メッセージ一覧
        this._protocolMessages = new ProtocolMessages();

        // 遊具
        this._playeq = new PlaygroundEquipment();

        // ユーザーコントロール
        this._userCtrl = new UserCtrl(this._playeq);

        // 審判コントロール
        this._judgeCtrl = new JudgeCtrl(this._playeq, this._userCtrl);

        // どちらかが勝ったとき
        this._judgeCtrl.onWon = (myPiece) => {
            let response = this.protocolMessages.createWon(myPiece);
            this._connection.webSock1.send(JSON.stringify(response));
        };

        // 引き分けたとき
        this._judgeCtrl.onDraw = () => {
            let response = this.protocolMessages.createDraw();
            this._connection.webSock1.send(JSON.stringify(response));
        };

        this.connect();
    }

    setup(setLabelOfButton) {
        // １手進めたとき
        this._userCtrl.onDoMove = (sq, myPiece) => {
            // ボタンのラベルを更新
            setLabelOfButton(sq, myPiece);

            let response = this.protocolMessages.createDoMove(sq, myPiece);
            this._connection.webSock1.send(JSON.stringify(response));
        };
    }

    /**
     * 接続
     */
    get connection() {
        return this._connection;
    }

    /**
     * メッセージ一覧
     */
    get protocolMessages() {
        return this._protocolMessages;
    }

    /**
     * 遊具
     */
    get playeq() {
        return this._playeq;
    }

    /**
     * ユーザーコントロール
     */
    get userCtrl() {
        return this._userCtrl;
    }

    /**
     * 審判コントロール
     */
    get judgeCtrl() {
        return this._judgeCtrl;
    }

    /**
     * 接続
     */
    connect() {
        this._connection.connect(
            // Webソケットを開かれたとき
            () => {
                console.log("WebSockets connection created.");
                let response = this.protocolMessages.createStart();
                this._connection.webSock1.send(JSON.stringify(response));
            },
            // Webソケットが閉じられたとき
            (e) => {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`);
                // 1回だけ再接続を試みます
                this._reconnect();
            },
            // サーバーからのメッセージを受信したとき
            this._onSetMessageFromServer,
            // エラー時
            (e) => {
                console.log(`Socket is error. ${e.reason}`);
            }
        );
    }
}
```

# Step 10. 通信プロトコル作成 - protocol_main.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄connection.js
                │           ├── 📄engine.js
                │           ├── 📄game_rule.js
                │           ├── 📄judge_ctrl.js
👉              │           ├── 📄protocol_main.js
                │           ├── 📄protocol_messages.js
                │           └── 📄user_ctrl.js
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
        // console.log(`[Debug][setMessage] event=${event} text=${text} sq=${sq} myPiece=${myPiece} winner=${winner}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "StoC_Start":
                // 対局開始の一斉通知
                vue1.init(); // 画面を初期化
                break;

            case "StoC_End":
                // 対局終了の一斉通知
                let result;
                if (winner == PC_EMPTY_LABEL) {
                    result = RESULT_DRAW;
                } else if (winner == vue1.engine.connection.myPiece) {
                    result = RESULT_WON;
                } else {
                    result = RESULT_LOST;
                }

                vue1.setGameIsOver(result);
                break;

            case "StoC_Move":
                // 指し手の一斉通知
                if (myPiece != vue1.engine.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    vue1.engine.userCtrl.doMove(parseInt(sq), myPiece);
                    vue1.engine.judgeCtrl.doJudge(myPiece);

                    // 自分の手番に変更
                    vue1.engine.userCtrl.isMyTurn = true;
                    vue1.engine.userCtrl.isWaitForOther = false;
                }
                break;

            default:
                console.log("No event");
        }
    };
}
```

# Step 11. 対局申込画面作成 - match_request.html ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
👉                          └── match_request.html
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

                            <!-- 部屋名 -->
                            <v-text-field required v-model="roomName.value" :rules="roomName.rules" counter="25" hint="A-Z, a-z, 0-9, No number at the beginning. Max 25 characters" label="Room name" name="room_name"></v-text-field>

                            <!-- X か O -->
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
                    roomName: {
                        value: "Elephant",
                        rules: [
                            (v) => v.length <= 25 || "Max 25 characters", // 文字数上限
                            (value) => {
                                const pattern = /^[A-Za-z][A-Za-z0-9]*$/; // 正規表現で指定
                                return pattern.test(value) || "Invalid format";
                            },
                        ],
                    },
                    selectedMyPiece: "X",
                    pieces: ["X", "O"],
                },
            });
        </script>
    </body>
</html>
```

# Step 12. 対局画面作成 - play_base.html ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
                            ├── match_request.html
👉                          └── play_base.html
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
                                    {% comment %} Vue で二重波括弧（braces）は変数の展開に使っていることから、 Python のテンプレートに二重波括弧を変数の展開に使わないよう verbatim で指示します。 {% endcomment %}
                                    <!-- -->
                                    {% verbatim %}
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
                    {% block footer_section1 %}
                    <!-- あれば、ここにボタンを置く -->
                    {% endblock footer_section1 %}
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

        <script src="{% static 'webapp1/tic-tac-toe/v2/connection.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/engine.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/game_rule.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/judge_ctrl.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/playground_equipment.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/protocol_main.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/protocol_messages.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/user_ctrl.js' %}"></script>

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
                    engine: new Engine(
                        createSetMessageFromServer(),
                        packReconnect(),
                        // 部屋名
                        document.forms["form1"]["room_name"].value,
                        // X か O
                        document.forms["form1"]["my_piece"].value,
                        // 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
                        (roomName, myPiece) => {
                            // 接続文字列
                            const connectionString = `ws://${window.location.host}/tic-tac-toe/v2/play/${roomName}/`;
                            //                                                                  ^
                            //                        ----]----------------------]---------------------------------
                            //                        1    2                      3
                            // 1. プロトコル（Web socket）
                            // 2. ホスト アドレス
                            // 3. パス
                            // console.log(`[Debug] new Engine ... roomName=${roomName} myPiece=${myPiece} connectionString=${connectionString}`);

                            return connectionString;
                        }
                    ),
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

                        this.engine.setup(this.packSetLabelOfButton());

                        this.setState(STATE_DURING_GAME);

                        this.engine.userCtrl.init(this.engine.connection.myPiece);

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
                        // console.log(`[Debug] Vue#clickSquare sq=${sq} this.engine.userCtrl.isMyTurn=${this.engine.userCtrl.isMyTurn}`);

                        if (this.engine.playeq.getPieceBySq(sq) == PC_EMPTY) {
                            if (!this.engine.userCtrl.isMyTurn) {
                                // Wait for other to place the move
                                console.log("Wait for other to place the move");
                                this.engine.userCtrl.isWaitForOther = true;
                            } else {
                                this.engine.userCtrl.isMyTurn = false;

                                this.engine.userCtrl.doMove(parseInt(sq), this.engine.connection.myPiece);
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
                     * @return {*} ラムダ関数
                     */
                    packSetLabelOfButton() {
                        return (sq, piece) => {
                            this.setLabelOfButton(sq, piece);
                        };
                    },
                    /**
                     *
                     */
                    setState(state) {
                        this.state = state;
                    },
                    /**
                     * 対局は終了しました
                     */
                    setGameIsOver(result) {
                        // console.log(`[Debug][setGameIsOver] result=${result}`);

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
                        return this.state == STATE_DURING_GAME && this.engine.userCtrl.isMyTurn;
                    },
                    isAlertWaitForOther() {
                        return this.engine.userCtrl.isWaitForOther;
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
                    {% block method_section1 %}
                    // あれば、ここにメソッドを置く
                    {% endblock method_section1 %}
                },
            });
        </script>
    </body>
</html>
```

# Step 13. 対局画面作成 - play.html.txt ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
                            ├── match_request.html
                            ├── play_base.html
👉                          └── play.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "tic-tac-toe/v2/play_base.html" %}
{#          -----------------------------
            1
1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/play_base.html
                                   -----------------------------

    自動フォーマットしないでください
    Do not auto fomatting
#}

{% block footer_section1 %}
                    <v-container>
                        <v-btn block elevation="2" v-on:click="clickPlayAgain()" :disabled="isDisabledPlayAgainButton()"> Play again </v-btn>
                    </v-container>
{% endblock footer_section1 %}

{% block method_section1 %}
                    /**
                     *
                     */
                    clickPlayAgain() {
                        console.log(`Play Again`);
                        this.init();
                    },
                    /**
                     * Play again ボタンは非表示か
                     */
                    isDisabledPlayAgainButton() {
                        switch (this.state) {
                            case STATE_GAME_IS_OVER:
                                return false; // Enable
                            default:
                                return true; // Disable
                        }
                    },
{% endblock method_section1 %}
```

# Step 14. 通信プロトコル作成 - protocol.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── match_request.html
            │               └── play.html
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      └── protocol.py
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

# Step 15. Webソケットの通信プロトコル作成 - consumer.py ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── match_request.html
            │               └── play.html
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      ├── consumer1.py
                        └── protocol.py
```

```py
# 参考にした記事
# -------------
# 📖[Django Channels and WebSockets](https: // blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from webapp1.websocks.tic_tac_toe.v2.protocol import TicTacToeV2Protocol
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV2Consumer(AsyncJsonWebsocketConsumer):
    #           ^

    def __init__(self):
        super().__init__()
        self.protocol = TicTacToeV2Protocol()

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

# Step 16. ビュー編集 - v_tic_tac_toe_v2.py ファイル

以下のファイルを新規作成してほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── match_request.html
            │               └── play.html
            ├── 📂views
👉          │   └── v_tic_tac_toe_v2.py
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── consumer1.py
                        └── protocol.py
```

```py
from django.http import Http404
from django.shortcuts import render, redirect


def render_match_request(request):
    """対局要求"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe/v2/play/{room_name}/?&mypiece={myPiece}')
        #                               ^
        #                 ----------------------------------------------------
        #                 1
        # 1. http://example.com:8000/tic-tac-toe/v2/play/Elephant/?&mypiece=X
        #                           -----------------------------------------
    return render(request, "webapp1/tic-tac-toe/v2/match_request.html", {})
    #                                            ^
    #                       -----------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_request.html
    #                            -----------------------------------------


def render_play(request, room_name):
    """対局画面"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "webapp1/tic-tac-toe/v2/play.html.txt", context)
    #                                            ^
    #                       ------------------------------------
    #                       1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/play.html.txt
    #                            ------------------------------------
```

# Step 17. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── match_request.html
            │               └── play.html
            ├── 📂views
            │   └── v_tic_tac_toe_v2.py
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v2
            │           ├── consumer1.py
            │           └── protocol.py
👉          └── urls.py
```

👇追加する部分のみ抜粋

```py
from django.urls import path

from webapp1.views import v_tic_tac_toe_v2
#    ------- -----        ----------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...略...

    # 対局要求
    path('tic-tac-toe/v2/match-request/', v_tic_tac_toe_v2.render_match_request),
    #                  ^                                 ^
    #     -----------------------------   -------------------------------------
    #     1                               2
    # 1. URLの `tic-tac-toe/v2/match-request/` というパスにマッチする
    # 2. v_tic_tac_toe_v2.py ファイルの render_match_request メソッド

    # 対局中
    path('tic-tac-toe/v2/play/<str:room_name>/', v_tic_tac_toe_v2.render_play),
    #                  ^                                        ^
    #     ------------------------------------   ----------------------------
    #     1                                      2
    # 1. URLの `tic-tac-toe/v2/play/<部屋名>/` というパスにマッチする。 <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. v_tic_tac_toe_v2.py ファイルの render_play メソッド
]
```

# Step 18. ルート編集 - routing1.py ファイル

以下のファイルを無ければ作成、あればマージしてほしい。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄protocol_main.js
            │   │           ├── 📄protocol_messages.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── match_request.html
            │               └── play.html
            ├── 📂views
            │   └── v_tic_tac_toe_v2.py
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v2
            │           ├── consumer1.py
            │           └── protocol.py
👉          ├── routing1.py
            └── urls.py
```

👇追加する部分のみ抜粋

```py
# 〇×ゲームの練習２
from webapp1.websocks.tic_tac_toe.v2.consumer import TicTacToeV2Consumer
#                                  ^                           ^
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# ...中略...

websocket_urlpatterns = [

    # ...中略...

    # 〇×ゲームの練習２
    url(r'^tic-tac-toe/v2/play/(?P<room_name>\w+)/$',
        #               ^
        # -----------------------------------------
        # 1
        TicTacToeV2Consumer.as_asgi()),
    #             ^
    #   -----------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/play/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
```

# Step 19. Web画面へアクセス

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください。  

📖 [http://localhost:8000/tic-tac-toe/v2/match-request/](http://localhost:8000/tic-tac-toe/v2/match-request/)  

# 次の記事

* 📖 [Django さくらVPS 備忘録](https://qiita.com/muzudho1/items/1d3b4b5608716463184c)

# 参考にした記事

📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  
