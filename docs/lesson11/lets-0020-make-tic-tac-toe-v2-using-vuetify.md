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

# Step 3. 物の定義 - things.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
👉              │           └── things.js
                └── 🚀favicon.ico
```

```js
// +--------
// | 駒
// |

/**
 * PC は Piece （駒）の略です
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

// |
// | 駒
// +--------

// +--------
// | 盤
// |

/**
 * 盤上の升の数
 * @type {number}
 */
const BOARD_AREA = 9;

/**
 * SQ は Square （マス）の略です
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
 * 盤
 */
class Board {
    constructor() {
        // 各マス
        this._squares = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];
    }

    /**
     * 盤上のマス番号で示して、駒を取得
     * @param {number} sq - マス番号
     */
    getPieceBySq(sq) {
        return this._squares[sq];
    }

    /**
     * 盤上のマスに駒を上書きします
     *
     * @param {*} sq - マス番号
     * @param {*} piece - 駒
     */
    setPiece(sq, piece) {
        this._squares[sq] = piece;
    }
}

// | 盤
// |
// +--------

// +--------
// | 棋譜
// |

/**
 * 棋譜
 */
class Record {
    constructor() {
        this._squares = [];
    }

    /**
     *
     * @param {*} sq - 駒を置いた場所
     */
    push(sq) {
        this._squares.push(sq);
    }

    pop() {
        this._squares.pop();
    }

    get length() {
        return this._squares.length;
    }
}

// | 棋譜
// |
// +--------
```

# Step 4. 概念の定義 - concepts.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
👉              │           ├── concepts.js
                │           └── things.js
                └── 🚀favicon.ico
```

```js
/**
 * 部屋の状態
 */
class RoomState {
    /**
     * ゲームしてません
     */
    static get none() {
        return 0;
    }

    /**
     * ゲーム中
     */
    static get playing() {
        return 1;
    }

    /**
     * 生成
     * @param {int} value
     * @param {function} changeValue - 値の変更
     */
    constructor(value, changeValue) {
        console.log(`[RoomState constructor]`);

        this._value = value;
        this._changeValue = changeValue;
    }

    /**
     * 値
     */
    get value() {
        return this._value;
    }

    set value(value) {
        console.log(`[RoomState set value]`);

        if (this._value === value) {
            return;
        }

        let oldValue = this._value;
        this._value = value;
        this._changeValue(oldValue, this._value);
    }
}

/**
 * 自分のターン
 */
class MyTurn {
    /**
     * 生成
     * @param {*} myPiece - 自分の駒。 "X", "O", "_"
     */
    constructor(myPiece) {
        // 自分の手番か（初回は先手）
        this._isTrue = myPiece == PC_X_LABEL;
    }

    /**
     * 真実か？
     */
    get isTrue() {
        return this._isTrue;
    }

    set isTrue(value) {
        this._isTrue = value;
        vue1.raiseMyTurnChanged();
    }
}

/**
 * ゲームオーバー状態
 *
 * * 自分視点
 */
class GameoverSet {
    /**
     * ゲームオーバーしてません
     */
    static get none() {
        return 0;
    }

    /**
     * 勝ち
     */
    static get win() {
        return 1;
    }

    /**
     * 引き分け
     */
    static get draw() {
        return 2;
    }

    /**
     * 負け
     */
    static get lose() {
        return 3;
    }

    /**
     * 生成
     * @param {int} value
     */
    constructor(value) {
        this._value = value;
    }

    /**
     * 値
     */
    get value() {
        return this._value;
    }

    set value(value) {
        this._value = value;
    }
}
```

# Step 5. ゲームルール定義 - game_rule.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── concepts.js
                │           ├── connection.js
👉              │           ├── game_rule.js
                │           ├── message_sender.js
                │           └── things.js
                └── 🚀favicon.ico
```

```js
/**
 * ゲーム状態
 */
const GAME_STATE_DURING = "DuringGame";
const GAME_STATE_IS_OVER = "GameIsOver";

/**
 * 駒が３つ並んでいるパターン
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

/**
 * 手番反転
 *
 * @param {*} piece
 * @returns
 */
function flipTurn(piece) {
    if (piece == PC_X_LABEL) {
        return PC_O_LABEL;
    } else if (piece == PC_O_LABEL) {
        return PC_X_LABEL;
    }

    return piece;
}
```

# Step 6. プロトコル実装 - message_sender.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── concepts.js
👉              │           ├── message_sender.js
                │           └── things.js
                └── 🚀favicon.ico
```

```js
/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class MessageSender {
    /**
     * どちらかのプレイヤーが駒を置いたとき
     * @param {int} sq - 升番号
     * @param {string} pieceMoved - 駒を置いたプレイヤー。 X か O
     * @returns メッセージ
     */
    createDoMove(sq, pieceMoved) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        console.log(`[MessageSender createDoMove] sq=${sq} pieceMoved=${pieceMoved}`);
        return {
            c2s_event: "C2S_Moved",
            c2s_sq: sq,
            c2s_pieceMoved: pieceMoved,
        };
    }

    /**
     * 引き分けたとき、とりあえず両方のプレイヤーが、サーバーへ対局終了メッセージを送ります
     * @returns メッセージ
     */
    createDraw() {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_End",
            c2s_winner: PC_EMPTY_LABEL,
        };
    }

    /**
     * 対局を開始したとき
     * @returns メッセージ
     */
    createStart() {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_Start",
        };
    }

    /**
     * 勝った方のプレイヤーが、サーバーに対局終了メッセージを送ります
     * @param {*} pieceMoved - 駒を置いた方の X か O
     * @returns メッセージ
     */
    createWon(pieceMoved) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_End",
            c2s_winner: pieceMoved,
        };
    }
}
```

# Step 7. 通信接続の作成 - connection.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── concepts.js
👉              │           ├── connection.js
                │           ├── message_sender.js
                │           └── things.js
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

# Step 8. 遊具作成 - playground_equipment.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── concepts.js
                │           ├── connection.js
                │           ├── game_rule.js
👉              │           ├── playground_equipment.js
                │           ├── message_sender.js
                │           └── things.js
                └── 🚀favicon.ico
```

```js
/**
 * 遊具
 */
class PlaygroundEquipment {
    constructor() {
        // あとで onStart(...) を呼出してください
    }

    /**
     * 対局開始時
     *
     * @param {string} myPiece - "X", "O", "_"
     */
    onStart(myPiece) {
        console.log(`[PlaygroundEquipment onStart] myPiece=${myPiece} PC_EMPTY=${PC_EMPTY} PC_X_LABEL=${PC_X_LABEL}`);

        // 盤面
        this._board = new Board();

        // 棋譜
        this._record = new Record();

        // 自分の手番
        this._myTurn = new MyTurn(myPiece);

        // ゲームオーバー状態
        this._gameoverState = new GameoverSet(GameoverSet.none);
    }

    /**
     * 盤
     */
    get board() {
        return this._board;
    }

    /**
     * 棋譜
     */
    get record() {
        return this._record;
    }

    /**
     * 自分のターン
     */
    get myTurn() {
        return this._myTurn;
    }

    /**
     * ゲームオーバー状態
     */
    get gameoverState() {
        return this._gameoverState;
    }

    /**
     * マスがすべて埋まっていますか
     */
    isBoardFill() {
        return this.record.length == 9;
    }

    /**
     * 同じ駒が３個ありますか
     */
    isThere3SamePieces() {
        return 5 <= this.record.length;
    }
}
```

# Step 9. ユーザーコントロール作成 - user_ctrl.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄concepts.js
                │           ├── 📄connection.js
                │           ├── 📄game_rule.js
                │           ├── 📄message_sender.js
                │           ├── 📄things.js
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

        // イベントリスナー
        this._onDoMove = () => {};
    }

    /**
     * 駒を置いたとき
     */
    set onDoMove(func) {
        this._onDoMove = func;
    }

    /**
     * 駒を置きます
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} piece - X か O
     * @returns 駒を置けたら真、それ以外は偽
     */
    doMove(sq, piece) {
        if (this._playeq.gameoverState.value != GameoverSet.none) {
            // ゲームオーバー後に駒を置いてはいけません
            console.log(`warning of illegal move. gameoverState=${this._playeq.gameoverState.value}`);
            return false;
        }

        if (this._playeq.board.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら駒を置きます

            this._playeq.record.push(sq); // 棋譜に追加

            // 駒を置きます
            switch (piece) {
                case PC_X_LABEL:
                    this._playeq.board.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    this._playeq.board.setPiece(sq, PC_O);
                    break;
                default:
                    alert(`[Error] Invalid piece = ${piece}`);
                    return false;
            }

            console.log(`[UserCtrl doMove] sq=${sq} piece=${piece}`);
            this._onDoMove(sq, piece);
        }

        return true;
    }
}
```

# Step 10. 審判作成 - judge_ctrl.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄concepts.js
                │           ├── 📄connection.js
                │           ├── 📄game_rule.js
👉              │           ├── 📄judge_ctrl.js
                │           ├── 📄message_sender.js
                │           ├── 📄things.js
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

        // 判断したとき
        this._onJudged = (pieceMoved, gameoverSet) => {};
    }

    /**
     * 判断したとき
     */
    set onJudged(func) {
        this._onJudged = func;
    }

    /**
     * ゲームオーバー判定
     */
    doJudge(piece_moved) {
        let gameoverSet = this.#makeGameoverSet();
        console.log(`[doJudge] gameoverSet=${gameoverSet}`);
        this._onJudged(piece_moved, gameoverSet);
    }

    /**
     * ゲームオーバー判定
     *
     * * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください
     *
     * @returns ゲームオーバー状態
     */
    #makeGameoverSet() {
        console.log(`[#makeGameoverSet] isThere3SamePieces=${this._playeq.isThere3SamePieces()}`);
        if (this._playeq.isThere3SamePieces()) {
            // 先手番が駒を３つ置いてから、判定を始めます
            for (let squaresOfWinPattern of WIN_PATTERN) {
                // 勝ちパターンの１つについて
                console.log(`[#makeGameoverSet] this.#isPieceInLine(squaresOfWinPattern)=${this.#isPieceInLine(squaresOfWinPattern)}`);
                if (this.#isPieceInLine(squaresOfWinPattern)) {
                    // 当てはまるなら
                    console.log(`[#makeGameoverSet] this._playeq.myTurn.isTrue=${this._playeq.myTurn.isTrue}`);
                    if (this._playeq.myTurn.isTrue) {
                        // 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return GameoverSet.lose;
                    } else {
                        // 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return GameoverSet.win;
                    }
                }
            }
        }

        // 勝ち負けが付かず、盤が埋まったら引き分け
        if (this._playeq.isBoardFill()) {
            return GameoverSet.draw;
        }

        // ゲームオーバーしてません
        return GameoverSet.none;
    }

    /**
     * 駒が３つ並んでいるか？
     * @param {*} squaresOfWinPattern - 勝ちパターン
     * @returns 並んでいれば真、それ以外は偽
     */
    #isPieceInLine(squaresOfWinPattern) {
        return (
            this._playeq.board.getPieceBySq(squaresOfWinPattern[0]) !== PC_EMPTY && //
            this._playeq.board.getPieceBySq(squaresOfWinPattern[0]) === this._playeq.board.getPieceBySq(squaresOfWinPattern[1]) &&
            this._playeq.board.getPieceBySq(squaresOfWinPattern[0]) === this._playeq.board.getPieceBySq(squaresOfWinPattern[2])
        );
    }
}
```

# Step 11. ゲームエンジン作成 - engine.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄concepts.js
                │           ├── 📄connection.js
👉              │           ├── 📄engine.js
                │           ├── 📄game_rule.js
                │           ├── 📄judge_ctrl.js
                │           ├── 📄message_sender.js
                │           ├── 📄things.js
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
     * @param {*} setMessageFromServer - サーバーからのメッセージをセットする関数
     * @param {*} reconnect - 再接続ラムダ関数
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
     */
    constructor(setMessageFromServer, reconnect, roomName, myPiece, convertPartsToConnectionString) {
        this._setMessageFromServer = setMessageFromServer;
        this._reconnect = reconnect;

        // 自分の駒
        this._myPiece = myPiece;

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

        // 接続
        this._connection = new Connection();
        this._connection.setup(roomName, myPiece, convertPartsToConnectionString);

        // メッセージ一覧
        this._messageSender = new MessageSender();

        // 遊具
        this._playeq = new PlaygroundEquipment();

        // ユーザーコントロール
        this._userCtrl = new UserCtrl(this._playeq);

        // 審判コントロール
        this._judgeCtrl = new JudgeCtrl(this._playeq, this._userCtrl);

        // 判断したとき
        this._judgeCtrl.onJudged = (pieceMoved, gameoverSet) => {
            this._playeq.gameoverState.value = gameoverSet;
            let response;

            switch (gameoverSet) {
                case GameoverSet.win:
                    // 勝ったとき
                    response = this.messageSender.createWon(pieceMoved);
                    this._connection.webSock1.send(JSON.stringify(response));
                    break;
                case GameoverSet.draw:
                    // 引き分けたとき
                    response = this.messageSender.createDraw();
                    this._connection.webSock1.send(JSON.stringify(response));
                    break;
                case GameoverSet.lose:
                    // 負けたとき
                    break;
                case GameoverSet.none:
                    // なんでもなかったとき
                    break;
                default:
                    throw new Error(`Unexpected gameoverSet=${gameoverSet}`);
            }
        };

        this.connect();
    }

    setup(setLabelOfButton) {
        // １手進めたとき
        this._userCtrl.onDoMove = (sq, pieceMoved) => {
            // ボタンのラベルを更新
            setLabelOfButton(sq, pieceMoved);

            console.log(`[onDoMove] this._myPiece=${this._myPiece} pieceMoved=${pieceMoved}`);

            // 自分の指し手なら送信
            if (this._myPiece == pieceMoved) {
                let response = this.messageSender.createDoMove(sq, pieceMoved);
                this._connection.webSock1.send(JSON.stringify(response));
            }
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
    get messageSender() {
        return this._messageSender;
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
     * 勝者
     */
    get winner() {
        return this._winner;
    }

    set winner(value) {
        this._winner = value;
    }

    /**
     * 対局結果
     */
    getGameoverSet() {
        // 勝者 "X", "O" を、勝敗 WIN, DRAW, LOSE, NONE に変換

        if (this._winner == PC_EMPTY_LABEL) {
            return GameoverSet.draw;
        } else if (this._winner == vue1.engine.connection.myPiece) {
            return GameoverSet.win;
        } else if (this._winner == flipTurn(vue1.engine.connection.myPiece)) {
            return GameoverSet.lose;
        }

        return GameoverSet.none;
    }

    /**
     * 接続
     */
    connect() {
        this._connection.connect(
            // Webソケットを開かれたとき
            () => {
                console.log("WebSockets connection created.");
                let response = this.messageSender.createStart();
                this._connection.webSock1.send(JSON.stringify(response));
            },
            // Webソケットが閉じられたとき
            (e) => {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`);
                // 1回だけ再接続を試みます
                this._reconnect();
            },
            // サーバーからのメッセージを受信したとき
            this._setMessageFromServer,
            // エラー時
            (e) => {
                console.log(`Socket is error. ${e.reason}`);
            }
        );
    }

    /**
     * 開始時
     */
    onStart() {
        console.log(`[Engine onStart] myPiece=${this._connection.myPiece}`);
        this._winner = "";

        this._playeq.onStart(this._connection.myPiece);
    }
}
```

# Step 12. 通信プロトコル作成 - message_receiver.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂static
                ├── 📂webapp1
                │   └── 📂tic-tac-toe
                │       └── 📂v2
                │           ├── 📄concepts.js
                │           ├── 📄connection.js
                │           ├── 📄engine.js
                │           ├── 📄game_rule.js
                │           ├── 📄judge_ctrl.js
👉              │           ├── 📄message_receiver.js
                │           ├── 📄message_sender.js
                │           ├── 📄things.js
                │           └── 📄user_ctrl.js
                └── 🚀favicon.ico
```

```js
/**
 * サーバーからクライアントへ送られてきたメッセージをセットする関数を返します
 * @returns 関数
 */
function packSetMessageFromServer() {
    return (message) => {
        // `s2c_` は サーバーからクライアントへ送られてきた変数の目印
        // イベント
        let event = message["s2c_event"];
        // 升番号
        let sq = message["s2c_sq"];
        // 手番。 "X" か "O"
        let piece_moved = message["s2c_pieceMoved"];
        // 勝者
        let winner = message["s2c_winner"];
        console.log(`[setMessage] サーバーからのメッセージを受信しました event=${event} sq=${sq} piece_moved=${piece_moved} winner=${winner}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "S2C_Start":
                // 対局開始時
                console.log(`[setMessage] S2C_Start`);
                vue1.onStart();
                break;

            case "S2C_End":
                // 対局終了時
                vue1.onGameover(winner);
                break;

            case "S2C_Moved":
                // 指し手受信時
                console.log(`[setMessage] S2C_Moved piece_moved=${piece_moved} myPiece=${vue1.engine.connection.myPiece}`);

                if (piece_moved != vue1.engine.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    vue1.engine.userCtrl.doMove(parseInt(sq), piece_moved);

                    // 自分の手番に変更
                    vue1.engine.playeq.myTurn.isTrue = true;

                    // アラートの非表示
                    vue1.isVisibleAlertWaitForOther = false;
                }

                // どちらの手番でもゲームオーバー判定は行います
                vue1.engine.judgeCtrl.doJudge(piece_moved);

                break;

            default:
                // Undefined behavior
                console.log(`[setMessage] ignored. event=[${event}]`);
        }
    };
}
```

# Step 13. 対局申込画面作成 - match_application.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
                │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
👉                          └── 📄match_application.html
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

                            <!-- `po_` は POST送信するパラメーター名の目印 -->
                            <!-- 部屋名 -->
                            <v-text-field name="po_room_name" required v-model="roomName.value" :rules="roomName.rules" counter="25" hint="A-Z, a-z, 0-9, No number at the beginning. Max 25 characters" label="Room name"></v-text-field>

                            <!--
                                自分の駒。 "X" か "O"。 機能拡張も想定

                                * 戻り値をオブジェクトのまま受け取りたいときは、タグの属性として return-object を付ける
                            -->
                            <v-select name="po_my_piece" v-model="visitor.value" :items="visitor.select" item-text="text" item-value="value" label="Your piece" persistent-hint single-line></v-select>

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
                    // 部屋名
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
                    // 入場者
                    visitor: {
                        // `dj_` は Djangoでレンダーするパラメーター名の目印
                        value: "{{dj_visitor_value}}",
                        select: JSON.parse("{{dj_visitor_select | escapejs}}"),
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 14. 対局画面作成 - playing_base.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
                            ├── 📄match_application.html
👉                          └── 📄playing_base.html
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
                        <h3>Welcome to room_{{dj_room_name}}</h3>
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

                        <!-- `po_` は POST送信するパラメーター名の目印 -->
                        <input type="hidden" name="po_room_name" value="{{dj_room_name}}" />
                        <input type="hidden" name="po_my_piece" value="{{dj_my_piece}}" />
                    </form>
                    {% block footer_section1 %}
                    <!-- ボタン等を追加したいなら、ここに挿しこめる -->
                    {% endblock footer_section1 %}
                    <v-container>
                        <v-alert type="info" color="green" v-show="isYourTurn">Your turn. Place your move <strong>{{dj_my_piece}}</strong></v-alert>
                        <v-alert type="warning" color="orange" v-show="isVisibleAlertWaitForOther">Wait for other to place the move</v-alert>
                        {% verbatim %}
                        <v-alert type="success" color="blue" v-show="isGameover">{{gameover_message}}</v-alert>
                        {% endverbatim %}
                        <v-alert type="warning" color="orange" v-show="isAlertReconnectingShow()">Reconnecting...</v-alert>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="{% static 'webapp1/tic-tac-toe/v2/things.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/concepts.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/connection.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/engine.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/game_rule.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/judge_ctrl.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/playground_equipment.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/message_receiver.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/message_sender.js' %}"></script>
        <script src="{% static 'webapp1/tic-tac-toe/v2/user_ctrl.js' %}"></script>
        <!--                    ===================================
                                1
        1. host1/webapp1/static/webapp1/tic-ta-toe/v2/user_ctrl.js
                 =================================================
        -->

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
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
                        packSetMessageFromServer(),
                        packReconnect(),
                        // `po_` は POST送信するパラメーター名の目印
                        // 部屋名
                        document.forms["form1"]["po_room_name"].value,
                        // 自分の駒。 X か O
                        document.forms["form1"]["po_my_piece"].value,
                        // 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
                        (roomName, myPiece) => {
                            // 接続文字列
                            // `dj_` は Djangoでレンダーするパラメーター名の目印
                            const connectionString = `ws://${window.location.host}{{dj_path_of_ws_playing}}${roomName}/`;
                            //                        ----]----------------------]-------------------------------------
                            //                        1    2                      3
                            // 1. プロトコル（Web socket）
                            // 2. ホスト アドレス
                            // 3. パス
                            console.log(`[Debug] new Engine ... roomName=${roomName} myPiece=${myPiece} connectionString=${connectionString}`);

                            return connectionString;
                        }
                    ),
                    state: GAME_STATE_DURING,
                    label0: PC_EMPTY_LABEL,
                    label1: PC_EMPTY_LABEL,
                    label2: PC_EMPTY_LABEL,
                    label3: PC_EMPTY_LABEL,
                    label4: PC_EMPTY_LABEL,
                    label5: PC_EMPTY_LABEL,
                    label6: PC_EMPTY_LABEL,
                    label7: PC_EMPTY_LABEL,
                    label8: PC_EMPTY_LABEL,
                    isYourTurn: false,
                    isGameover: false,
                    // 「相手の手番に着手しないでください」というアラートの可視性
                    isVisibleAlertWaitForOther: false,
                    roomState: new RoomState(RoomState.none,(oldValue, newValue)=>{
                        // changeRoomState
                        console.log(`[data roomState changeRoomState] state old=${oldValue} new=${newValue}`);
                        vue1.raiseRoomStateChanged();
                    }),
                    gameover_message : "",
                    messages: {
                        draw: "It's a draw.",
                        youLose: "You lose.",
                        youWin: "You win!",
                        {% block appendix_message %}
                        // メッセージを追加したければ、ここに挿しこめる
                        {% endblock appendix_message %}
                    }
                },
                // page loaded
                mounted: () => {
                    // ここで Vue の準備完了後の処理ができる。
                    // ただし、まだ this は初期化されてない
                },
                methods: {
                    // 対局開始時
                    onStart() {
                        console.log("[methods onStart]");

                        // 「相手の手番に着手しないでください」というアラートの非表示
                        this.isVisibleAlertWaitForOther = false;

                        this.engine.setup(this.packSetLabelOfButton());

                        this.engine.onStart();

                        this.roomState.value = RoomState.playing;

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
                        console.log(`[methods clickSquare] gameoverState=${this.engine.playeq.gameoverState.value}`);
                        if (this.engine.playeq.gameoverState.value != GameoverSet.none) {
                            // Ban on illegal move
                            console.log(`Ban on illegal move. gameoverState=${this.engine.playeq.gameoverState.value}`);
                            return;
                        }

                        if (this.engine.playeq.board.getPieceBySq(sq) == PC_EMPTY) {
                            if (!this.engine.playeq.myTurn.isTrue) {
                                // Wait for other to place the move
                                console.log("Wait for other to place the move");
                                this.isVisibleAlertWaitForOther = true;
                            } else {
                                // （サーバーからの応答を待たず）相手の手番に変更します
                                this.engine.playeq.myTurn.isTrue = false;

                                // 自分の一手
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
                        // console.log(`[methods setLabelOfButton] sq=${sq} piece=${piece}`);

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
                     * 対局は終了しました
                     */
                    onGameover(winner) {
                        console.log(`[methods onGameover] winner=${winner}`);
                        this.engine.winner = winner;
                        this.roomState.value = RoomState.none; // 画面を対局終了状態へ

                        this.gameover_message = this.createGameoverMessage();
                    },
                    /**
                     * ゲームオーバー時のメッセージ作成
                     */
                    createGameoverMessage() {
                        {% block create_gameover_message %}
                        // 返却値を変えたいなら、ここに挿しこめる
                        {% endblock create_gameover_message %}

                        // サーバーから勝者が送られてきているので、勝敗に変換
                        let gameover_set = this.engine.getGameoverSet();
                        // console.log(`[Debug][onGameover] gameover_set=${gameover_set}`);

                        switch (gameover_set) {
                            case GameoverSet.draw:
                                return this.messages.draw;
                            case GameoverSet.win:
                                return this.messages.youWin;
                            case GameoverSet.lose:
                                return this.messages.youLose;
                            case GameoverSet.none:
                                // ここに来るのはおかしい
                                return "";
                            default:
                                throw `unknown gameover_set = ${gameover_set}`;
                        }
                    },
                    /**
                     * (1) 対局中か
                     * (2) 自分の手番か
                     */
                    updateYourTurn(){
                        console.log(`[methods updateYourTurn 1] this.roomState=${this.roomState.value} this.engine.playeq.myTurn.isTrue=${this.engine.playeq.myTurn.isTrue}`);
                        let isYourTurn = this.roomState.value == RoomState.playing && this.engine.playeq.myTurn.isTrue;

                        {% block isYourTurn_patch1 %}
                        // 条件を追加したいなら、ここに挿しこめる
                        {% endblock isYourTurn_patch1 %}

                        console.log(`[methods updateYourTurn 2] isYourTurn=${isYourTurn}`);

                        // v-show="" は複雑なメソッドを指定すると動かないようなので、プロパティにします
                        this.isYourTurn = isYourTurn;
                    },
                    raiseRoomStateChanged() {
                        console.log(`[methods raiseRoomStateChanged] roomState=${this.roomState.value}`);
                        this.isGameover = this.roomState.value == RoomState.none;

                        this.updateYourTurn();
                    },
                    raiseMyTurnChanged() {
                        console.log(`[methods raiseMyTurnChanged]`);
                        this.updateYourTurn();
                    },
                    /**
                     * 再接続中表示中なら、アラートを常時表示
                     */
                    isAlertReconnectingShow() {
                        return this.engine.connection.isReconnectingDisplay;
                    },
                    {% block methods_footer %}
                    // メソッドを追加したければ、ここに挿しこめる
                    {% endblock methods_footer %}
                },
            });
        </script>
    </body>
</html>
```

# Step 15. 対局画面作成 - playing.html.txt ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            └── 📂templates
                └── 📂webapp1               # アプリケーション フォルダーと同じ名前
                    └── 📂tic-tac-toe
                        └── 📂v2
                            ├── 📄match_application.html
                            ├── 📄playing_base.html
👉                          └── 📄playing.html.txt
```

👇 自動フォーマットされてくないので、拡張子をテキストファイルにしておく  

```html
{% extends "tic-tac-toe/v2/playing_base.html" %}
{#          --------------------------------
            1
1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/playing_base.html
                                   --------------------------------

    自動フォーマットしないでください
    Do not auto fomatting
#}

{% block footer_section1 %}
    <v-container>
        <v-btn block elevation="2" v-on:click="clickPlayAgain()" :disabled="isDisabledPlayAgainButton()"> Play again </v-btn>
    </v-container>
{% endblock footer_section1 %}

{% block methods_footer %}
    /**
     *
     */
    clickPlayAgain() {
        console.log(`Play Again`);

        // 対局開始時
        this.onStart();
    },
    /**
     * Play again ボタンは非表示か
     */
    isDisabledPlayAgainButton() {
        switch (this.roomState.value) {
            case RoomState.none: // ゲームオーバー状態
                return false; // Enable
            default:
                return true; // Disable
        }
    },
{% endblock methods_footer %}
```

# Step 16. 通信プロトコル作成 - message_converter.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── 📄match_application.html
            │               ├── 📄playing_base.html
            │               └── 📄playing.html.txt
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      └── 📄message_converter.py
```

```py
class TicTacToeV2MessageConverter():
    """サーバープロトコル"""

    async def on_receive(self, scope, doc_received):
        """クライアントからサーバーへ送られてきた変数を解析し、
        サーバーからクライアントへ送信するメッセージの作成"""

        # ログインしていなければ AnonymousUser
        user = scope["user"]
        print(f"[TicTacToeV2MessageConverter on_receive] user=[{user}]")

        # `c2s_` は クライアントからサーバーへ送られてきた変数の目印
        event = doc_received.get("c2s_event", None)

        if event == 'C2S_End':
            # 対局終了時
            print(f"[TicTacToeV2MessageConverter on_receive] C2S_End")

            self.on_end(scope, doc_received)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': "S2C_End",
                # TODO 現状、クライアント側から勝者を送ってきているが、勝敗判定のロジックはサーバー側に置きたい
                's2c_winner': doc_received.get("c2s_winner", None),
            }

        elif event == 'C2S_Moved':
            # 駒を置いたとき
            # `s2c_` は サーバーからクライアントへ送る変数の目印
            c2s_sq = doc_received.get("c2s_sq", None)
            piece_moved = doc_received.get("c2s_pieceMoved", None)
            print(
                f"[TicTacToeV2MessageConverter on_receive] C2S_Moved c2s_sq=[{c2s_sq}] piece_moved=[{piece_moved}]")

            await self.on_move(scope, doc_received)

            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': 'S2C_Moved',
                's2c_sq': c2s_sq,
                's2c_pieceMoved': piece_moved,
            }

        elif event == 'C2S_Start':
            # 対局開始時
            print(f"[TicTacToeV2MessageConverter on_receive] C2S_Start")

            self.on_start(scope, doc_received)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': "S2C_Start",
            }

        raise ValueError(f"Unknown event: {event}")

    def on_end(self, scope, doc_received):
        """対局終了時"""
        # print("[TicTacToeV2MessageConverter on_end] ignored")
        pass

    async def on_move(self, scope, doc_received):
        """駒を置いたとき"""
        # print("[TicTacToeV2MessageConverter on_move] ignored")
        pass

    def on_start(self, scope, doc_received):
        """対局開始時"""
        # print("[TicTacToeV2MessageConverter on_start] ignored")
        pass
```

# Step 17. Webソケットの通信プロトコル作成 - consumer_base.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── 📄match_application.html
            │               ├── 📄playing_base.html
            │               └── 📄playing.html.txt
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      ├── 📄consumer_base.py
                        └── 📄message_converter.py
```

```py
# 参考にした記事
# -------------
# 📖[Django Channels and WebSockets](https: // blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TicTacToeV2ConsumerBase(AsyncJsonWebsocketConsumer):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()

    async def connect(self):
        """接続"""
        print("Connect")
        # ログインしていれば、ユーザーのPrimaryKeyは以下で取得可能。ログインしていなければ None
        # print(f'Connect self.scope["user"].pk={self.scope["user"].pk}')

        self.room_name = self.scope['url_route']['kwargs']['kw_room_name']
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

        # ちゃんと動いているようなら消す
        print(f"[TicTacToeV2ConsumerBase receive] text_data={text_data}")

        doc_received = json.loads(text_data)

        response = await self.on_receive(doc_received)

        # 部屋のメンバーに一斉送信します
        await self.channel_layer.group_send(self.room_group_name, response)

    async def on_receive(self, doc_received):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """
        return {}  # Empty

    async def send_message(self, message):
        """メッセージ送信"""
        await self.send(text_data=json.dumps({
            "message": message,
        }))
```

# Step 18. Webソケットの通信プロトコル作成 - consumer_custom.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── 📄match_application.html
            │               ├── 📄playing_base.html
            │               └── 📄playing.html.txt
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄consumer_base.py
👉                      ├── 📄consumer_custom.py
                        └── 📄message_converter.py
```

```py
from webapp1.websocks.tic_tac_toe.v2.consumer_base import TicTacToeV2ConsumerBase
#                                  ^ two                            ^ two
#    ------- ----------------------- -------------        -----------------------
#    1       2                       3                    4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.websocks.tic_tac_toe.v2.message_converter import TicTacToeV2MessageConverter
#                                  ^ two                                ^ two
#    ------- ----------------------- -----------------        ---------------------------
#    1       2                       3                        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV2ConsumerCustom(TicTacToeV2ConsumerBase):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()
        self._messageConverter = TicTacToeV2MessageConverter()

    async def on_receive(self, doc_received):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """

        return await self._messageConverter.on_receive(self.scope, doc_received)
```

# Step 19. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── 📄match_application.html
            │               ├── 📄playing_base.html
            │               └── 📄playing.html.txt
            ├── 📂views
            │   └── 📂tic_tac_toe
            │       └── 📂v2
👉          │           └── 📄resources.py
            └── 📂websocks
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄consumer_base.py
                        ├── 📄consumer_custom.py
                        └── 📄message_converter.py
```

```py
"""〇×ゲームの練習２"""
import json
from django.http import Http404
from django.shortcuts import render, redirect


# 以下、よく使う定型データ


# 対局申込 - 訪問後
match_application_open_context = {
    # `dj_` は Djangoでレンダーするパラメーター名の目印
    # 入場者データ
    "dj_visitor_value": "X",
    # Python と JavaScript 間で配列データを渡すために JSON 文字列形式にします
    "dj_visitor_select": json.dumps([
        {"text": "X", "value": "X"},
        {"text": "O", "value": "O"},
    ]),
}

# 対局中 - 駒
playing_expected_pieces = ['X', 'O']


# 以下、ロジック


class MatchApplication():
    """対局申込"""

    _path_of_http_playing = "/tic-tac-toe/v2/playing/{0}/?&mypiece={1}"
    #                                      ^ two
    #                        -----------------------------------------
    #                        1
    # 1. http://example.com:8000/tic-tac-toe/v2/playing/Elephant/?&mypiece=X
    #                           --------------------------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/match_application.html"
    #                                     ^ two
    #                ---------------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/match_application.html
    #                            ---------------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        return render_match_application(request, MatchApplication._path_of_http_playing, MatchApplication._path_of_html, MatchApplication.on_sent, MatchApplication.open)

    @staticmethod
    def on_sent(request):
        """送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass

    @staticmethod
    def open(request):
        """訪問後"""
        # 拡張したい挙動があれば、ここに書く

        return match_application_open_context


class Playing():
    """対局中"""

    _path_of_ws_playing = "/tic-tac-toe/v2/playing/"
    #                                    ^ two
    #                      ------------------------
    #                      1
    # 1. ws://example.com:8000/tic-tac-toe/v2/playing/
    #                         ------------------------

    _path_of_html = "webapp1/tic-tac-toe/v2/playing.html.txt"
    #                                     ^ two
    #                ---------------------------------------
    #                1
    # 1. host1/webapp1/templates/webapp1/tic-tac-toe/v2/playing.html.txt
    #                            ---------------------------------------

    @staticmethod
    def render(request, kw_room_name):
        """描画"""
        return render_playing(
            request,
            kw_room_name,
            Playing._path_of_ws_playing,
            Playing._path_of_html,
            Playing.on_update,
            playing_expected_pieces)

    @staticmethod
    def on_update(request):
        """訪問後または送信後"""
        # 拡張したい挙動があれば、ここに書く
        pass


# 以下、関数


def render_match_application(request, path_of_http_playing, path_of_html, on_sent, open):
    """対局申込 - 描画"""
    if request.method == "POST":
        # 送信後
        on_sent(request)

        # `po_` は POST送信するパラメーター名の目印
        po_room_name = request.POST.get("po_room_name")
        # 自分の駒。 "X" か "O"。 機能拡張も想定
        po_my_piece = request.POST.get("po_my_piece")

        # TODO バリデーションチェックしたい

        return redirect(path_of_http_playing.format(po_room_name, po_my_piece))

    # 訪問後
    context = open(request)

    return render(request, path_of_html, context)


def render_playing(request, kw_room_name, path_of_ws_playing, path_of_html, on_update, expected_pieces):
    """対局中 - 描画"""
    my_piece = request.GET.get("mypiece")
    if my_piece not in expected_pieces:
        raise Http404(f"My piece '{my_piece}' does not exists")

    on_update(request)

    # `dj_` は Djangoでレンダーするパラメーター名の目印
    context = {
        "dj_room_name": kw_room_name,
        "dj_my_piece": my_piece,
        "dj_path_of_ws_playing": path_of_ws_playing,
    }
    return render(request, path_of_html, context)
```

# Step 20. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── 📄match_application.html
            │               ├── 📄playing_base.html
            │               └── 📄playing.html.txt
            ├── 📂views
            │   └── 📂tic_tac_toe
            │       └── 📂v2
            │           └── 📄resources.py
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v2
            │           ├── 📄consumer_base.py
            │           ├── 📄consumer_custom.py
            │           └── 📄message_converter.py
👉          └── 📄urls.py
```

👇追加する部分のみ抜粋

```py
from django.urls import path

from webapp1.views.tic_tac_toe.v2 import resources as tic_tac_toe_v2
#    ------- --------------------        ---------    --------------
#    1       2                           3            4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. `3.` の別名

urlpatterns = [
    # ...略...

    # +----
    # | 〇×ゲーム２

    # 対局申込
    path('tic-tac-toe/v2/match-application/',
         #             ^
         # --------------------------------
         # 1
         tic_tac_toe_v2.MatchApplication.render),
    #                   ^
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/match-application/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v2 (別名)ファイルの MatchApplication クラスの render 静的メソッド

    # 対局中
    path('tic-tac-toe/v2/playing/<str:kw_room_name>/',
         #             ^
         # -----------------------------------------
         # 1
         tic_tac_toe_v2.Playing.render),
    #                 ^
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/playing/<部屋名>/` のような URL のパスの部分。
    #                              --------------------------------
    #    <部屋名> に入った文字列は kw_room_name 変数に渡されます
    # 2. tic_tac_toe_v2 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム２
    # +----
]
```

# Step 21. ルート編集 - routing1.py ファイル

以下の既存のファイルを編集してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂static
            │   ├── 📂webapp1
            │   │   └── 📂tic-tac-toe
            │   │       └── 📂v2
            │   │           ├── 📄concepts.js
            │   │           ├── 📄connection.js
            │   │           ├── 📄engine.js
            │   │           ├── 📄game_rule.js
            │   │           ├── 📄judge_ctrl.js
            │   │           ├── 📄message_receiver.js
            │   │           ├── 📄message_sender.js
            │   │           ├── 📄things.js
            │   │           └── 📄user_ctrl.js
            │   └── 🚀favicon.ico
            ├── 📂templates
            │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
            │       └── 📂tic-tac-toe
            │           └── 📂v2
            │               ├── 📄match_application.html
            │               ├── 📄playing_base.html
            │               └── 📄playing.html.txt
            ├── 📂views
            │   └── 📂tic_tac_toe
            │       └── 📂v2
            │           └── 📄resources.py
            ├── 📂websocks
            │   └── 📂tic-tac-toe
            │       └── 📂v2
            │           ├── 📄consumer_base.py
            │           ├── 📄consumer_custom.py
            │           └── 📄message_converter.py
👉          ├── 📄routing1.py
            └── 📄urls.py
```

👇追加する部分のみ抜粋

```py
# 〇×ゲームの練習２
from webapp1.websocks.tic_tac_toe.v2.consumer_custom import TicTacToeV2ConsumerCustom
#                                  ^ two                              ^ two
#    ------- ----------------------- ---------------        -------------------------
#    1       2                       3                      4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

# ...中略...

websocket_urlpatterns = [

    # ...中略...

    # 〇×ゲームの練習２
    url(r'^tic-tac-toe/v2/playing/(?P<kw_room_name>\w+)/$',
        #               ^
        # -----------------------------------------------
        # 1
        TicTacToeV2ConsumerCustom.as_asgi()),
    #             ^
    #   -----------------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v2/playing/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方。
    #    kw_room_name は変数として渡される
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
```

# Step 22. Web画面へアクセス

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください  

📖 [http://localhost:8000/tic-tac-toe/v2/match-application/](http://localhost:8000/tic-tac-toe/v2/match-application/)  

# 次の記事

* 📖 [Django さくらVPS 備忘録](https://qiita.com/muzudho1/items/1d3b4b5608716463184c)

# 参考にした記事

## Vuetify 関連

📖 [Vuetifyのv-selectにてitemsのキーがtextとvalueじゃないときの対処法](https://qiita.com/akido_/items/96ced6cd5fd9929c666f)  

## Web socket 関連

📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  
