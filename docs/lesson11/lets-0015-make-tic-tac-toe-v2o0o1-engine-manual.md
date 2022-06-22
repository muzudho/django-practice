# 目的

〇×ゲーム（Tic tac toe）の思考エンジンを作りたい  

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
| Frontend         | Vuetify                                   |
| Database         | Redis                                     |
| Editor           | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている  

```plaintext
    ├── 📂host_local1
    │    └── <いろいろ>
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂websocks
        │       │   └── 📂v1o1
        │       │       └── 📄consumer.py
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
        │       ├── 📄urls_ws1.py
        │       └── 📄urls.py
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄vuetify-desserts.json
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📂practice
        │   │       └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄routing1.py
        │   └── 📄urls.py
        ├── 📄asgi.py
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        └── 📄urls.py
```

以下、参考にした元記事は 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ  

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 物の定義 - things.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                └── 📂static
                    └── 📂tic_tac_toe       # アプリケーション フォルダーと同名
                        └── 📂v2o0o1
👉                          └── 📄things.js
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
const PC_EMPTY_LABEL = ".";
const PC_X_LABEL = "X";
const PC_O_LABEL = "O";

/**
 * 定数をラベルに変換
 *
 * @param {int} pc
 * @returns {str} label
 */
function pc_to_label(pc) {
    switch (pc) {
        case PC_EMPTY:
            return PC_EMPTY_LABEL;
        case PC_X:
            return PC_X_LABEL;
        case PC_O:
            return PC_O_LABEL;
        default:
            return pc;
    }
}

/**
 * ラベルを定数に変換
 *
 * @param {str} - label
 * @returns {int} - pc
 */
function label_to_pc(label) {
    switch (label) {
        case PC_EMPTY_LABEL:
            return PC_EMPTY;
        case PC_X_LABEL:
            return PC_X;
        case PC_O_LABEL:
            return PC_O;
        default:
            return label;
    }
}

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

    /**
     *
     * @returns コピー配列
     */
    toArray() {
        // スプレッド構文
        return [...this._squares];
    }

    /**
     * 盤面を設定します
     *
     * @param {*} token - Example: `..O.X....`
     */
    parse(token) {
        this._squares = token.split("").map((x) => label_to_pc(x));
    }

    /**
     * ダンプ
     */
    dump(indent) {
        return `
${indent}Board
${indent}-----
${indent}_squares:${this._squares}`;
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

    /**
     * 棋譜を設定します
     *
     * @param {*} token - Example: `53`
     */
    parse(token) {
        this._squares = token.split("").map((x) => parseInt(x));
    }

    /**
     * 棋譜を先頭から読取ります
     *
     * @param {function(int)} setSq - callback
     */
    forEach(setSq) {
        for (const sq of this._squares) {
            setSq(sq);
        }
    }

    /**
     * ダンプ
     */
    dump(indent) {
        return `
${indent}Record
${indent}------
${indent}_squares:${this._squares}`;
    }
}

// | 棋譜
// |
// +--------
```

# Step 3. 概念の定義 - concepts.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                └── 📂static
                    └── 📂tic_tac_toe
                        └── 📂v2o0o1
👉                          ├── 📄concepts.js
                            └── 📄things.js
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
     * @param {function} onChangeValue - 値の変更時
     */
    constructor(value, onChangeValue) {
        console.log(`[RoomState constructor]`);

        this._value = value;
        this._onChangeValue = onChangeValue;
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
        this._onChangeValue(oldValue, this._value);
    }

    /**
     * ダンプ
     * @param {str} indent
     * @returns
     */
    dump(indent) {
        return `
${indent}RoomState
${indent}---------
${indent}_value:${this._value}`;
    }
}

/**
 * 番
 */
class Turn {
    /**
     * 生成
     * @param {*} myTurn - 自分の手番。 "X", "O"
     */
    constructor(myTurn) {
        // 自分の手番
        this._me = myTurn;

        // 初期局面でコンストラクターが呼び出される想定で、"X" の方なら先手
        if (myTurn == PC_X_LABEL) {
            // 先手は自分
            this._next = myTurn;
        } else {
            // 先手は相手
            this._next = flipTurn(myTurn);
        }
    }

    /**
     * 自分の手番
     */
    get me() {
        return this._me;
    }

    /**
     * 次の番，手番
     */
    get next() {
        return this._next;
    }

    set next(value) {
        this._next = value;
    }

    /**
     * 私の番か？
     */
    get isMe() {
        return this._me == this._next;
    }

    /**
     * ダンプ
     * @param {str} indent
     * @returns
     */
    dump(indent) {
        return `
${indent}Turn
${indent}----
${indent}_me:${this._me}
${indent}_next:${this._next}
${indent}_isMe:${this._isMe}`;
    }
}

/**
 * ゲームオーバー集合
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
     * 勝った
     */
    static get won() {
        return 1;
    }

    /**
     * 引き分けた
     */
    static get draw() {
        return 2;
    }

    /**
     * 負けた
     */
    static get lost() {
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

    toString() {
        switch (this._value) {
            case GameoverSet.none:
                return "=\n.\n";
            case GameoverSet.won:
                return "= won\n.\n";
            case GameoverSet.draw:
                return "= draw\n.\n";
            case GameoverSet.lost:
                return "= lost\n.\n";
            default:
                throw Error(`[GameoverSet dump] Unexpected value=${this._value}`);
        }
    }

    /**
     * ダンプ
     * @param {str} indent
     * @returns
     */
    dump(indent) {
        return `
${indent}GameoverSet
${indent}-----------
${indent}_value:${this._value}
${indent}toString():${this.toString()}`;
    }
}

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

# Step 4. 局面作成 - position.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                └── 📂static
                    └── 📂tic_tac_toe
                        └── 📂v2o0o1
                            ├── 📄concepts.js
👉                          ├── 📄position.js
                            └── 📄things.js
```

```js
/**
 * 局面
 */
class Position {
    /**
     * 初期化
     *
     * * 対局開始時
     *
     * @param {string} myTurn - 自分の手番。 "X", "O"
     */
    constructor(myTurn) {
        console.log(`[Position constructor] 自分の手番=${myTurn}`);

        // 盤面
        this._board = new Board();

        // 棋譜
        this._record = new Record();

        // 番
        this._turn = new Turn(myTurn);
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
     * 番
     */
    get turn() {
        return this._turn;
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

    toBoardString() {
        // 何手目
        const moves = this._record.length + 1;

        // 手番
        let currentTurn;
        if (this._turn.isMe) {
            currentTurn = this._turn.me;
        } else {
            currentTurn = flipTurn(this._turn.me);
        }

        // 各マス
        const squares = this._board.toArray();
        console.log(`squares=${squares}`);
        const [a, b, c, d, e, f, g, h, i] = squares.map((x) => pc_to_label(x));

        return `= [Next ${moves} moves / ${currentTurn} turn]
. +---+---+---+
. | ${a} | ${b} | ${c} |
. +---+---+---+
. | ${d} | ${e} | ${f} |
. +---+---+---+
. | ${g} | ${h} | ${i} |
. +---+---+---+
. moves ${this._record.toMovesString()}
.
`;
    }

    /**
     * ダンプ
     */
    dump(indent) {
        return `
${indent}Position
${indent}--------
${indent}${this._board.dump(indent + "    ")}
${indent}${this._record.dump(indent + "    ")}
${indent}${this._turn.dump(indent + "    ")}`;
    }
}
```

# Step 5. ユーザーコントロール作成 - user_ctrl.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                └── 📂static
                    └── 📂tic_tac_toe
                        └── 📂v2o0o1
                            ├── 📄concepts.js
                            ├── 📄position.js
                            ├── 📄things.js
👉                          └── 📄user_ctrl.js
```

```js
/**
 * ユーザーコントロール
 */
class UserCtrl {
    /**
     * 初期化
     *
     * @param {function} onDidMove - 駒を置いたあと
     */
    constructor(onDidMove) {
        this._onDidMove = onDidMove;
    }

    /**
     * 駒を置きます
     *
     * @param {Position} position - 局面
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} piece - X か O
     * @returns 駒を置けたら真、それ以外は偽
     */
    doMove(position, piece, sq) {
        if (position.board.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら駒を置きます
            console.log(`[UserCtrl doMove] 置いたマス:${sq} 動かした駒:${piece}`);

            position.record.push(sq); // 棋譜に追加

            // 駒を置きます
            switch (piece) {
                case PC_X_LABEL:
                    position.board.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    position.board.setPiece(sq, PC_O);
                    break;
                default:
                    console.log(`[UserCtrl doMove] illegal move. invalid piece:${piece}`);
                    return false;
            }

            console.log(`[UserCtrl doMove] 反転前の手番=${position.turn.next}`);
            position.turn.next = flipTurn(position.turn.next);
            console.log(`[UserCtrl doMove] 反転後の手番=${position.turn.next}`);

            this._onDidMove(sq, piece);
            return true;
        }

        // 駒が置いてあるマスに駒は置けません
        console.log(`[UserCtrl doMove] illegal move. not empty square. sq:${sq}`);
        return false;
    }

    /**
     * 一手戻します
     *
     * @param {Position} position - 局面
     * @returns {bool} wasItDelete - 削除しました
     */
    undoMove(position) {
        const previousSq = position.record.pop();
        console.log(`[UserCtrl undoMove] previousSq:${previousSq}`);

        if (typeof previousSq === "undefined") {
            return false;
        }

        console.log(`[UserCtrl doMove] 反転前の手番:${position.turn.next}`);
        position.turn.next = flipTurn(position.turn.next);
        console.log(`[UserCtrl doMove] 反転後の手番:${position.turn.next}`);

        // 盤上の駒を消します
        position.board.setPiece(previousSq, PC_EMPTY);
        return true;
    }
}
```

# Step 6. 審判作成 - judge_ctrl.js ファイル

以下のファイルを作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                └── 📂static
                    └── 📂tic_tac_toe
                        └── 📂v2o0o1
                            ├── 📄concepts.js
👉                          ├── 📄judge_ctrl.js
                            ├── 📄position.js
                            ├── 📄things.js
                            └── 📄user_ctrl.js
```

```js
/**
 * 思考エンジン
 */
class Engine {
    /**
     * 生成
     * @param {string} myTurn - 自分の手番。 "X" か "O"。 部屋に入ると変えることができない
     * @param {UserCtrl} userCtrl - ユーザーコントロール
     * @param {JudgeCtrl} judgeCtrl - 審判コントロール
     */
    constructor(myTurn, userCtrl, judgeCtrl) {
        console.log(`[Engine constructor] 自分の手番=${myTurn}`);

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

        // 局面
        this._position = new Position(myTurn);

        // ゲームオーバー集合
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // ユーザーコントロール
        this._userCtrl = userCtrl;

        // 審判コントロール
        this._judgeCtrl = judgeCtrl;
    }

    /**
     * 局面
     */
    get position() {
        return this._position;
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
     * ゲームオーバー集合
     */
    get gameoverSet() {
        return this._gameoverSet;
    }

    set gameoverSet(value) {
        this._gameoverSet = value;
    }

    /**
     * 対局開始時
     */
    start() {
        console.log(`[Engine start] 自分の手番=${this._position.turn.me}`);

        // 勝者のクリアー
        this._winner = "";

        // ゲームオーバー状態のクリアー
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // 局面の初期化
        this._position = new Position(this._position.turn.me);
    }

    /**
     * コマンドの実行
     */
    execute(command) {
        let log = "";

        const lines = command.split(/\r?\n/);
        for (const line of lines) {
            // 空行はパス
            if (line.trim() === "") {
                continue;
            }

            // One line command
            log += "# " + line + "\n";

            const tokens = line.split(" ");
            switch (tokens[0]) {
                case "board":
                    // Example: `board`
                    log += this._position.toBoardString();
                    break;
                case "play":
                    // Example: `play X 2`
                    const isOk = this._userCtrl.doMove(this._position, tokens[1], parseInt(tokens[2]));
                    if (isOk) {
                        log += "=\n.\n";
                    } else {
                        log += "? err\n.\n";
                    }
                    break;
                case "judge":
                    // Example: `judge`
                    const gameoverSet = this._judgeCtrl.doJudge(this._position);
                    log += gameoverSet.toString();
                    break;
                default:
                    // ignored
                    break;
            }
        }

        return log;
    }

    dump(indent) {
        return `
${indent}Engine
${indent}------
${indent}_winner:${this._winner}
${indent}${this._gameoverSet.dump(indent + "    ")}
${indent}${this._position.dump(indent + "    ")}`;
    }
}
```

# Step 7. 思考エンジン作成 - engine.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                └── 📂static
                    └── 📂tic_tac_toe
                        └── 📂v2o0o1
                            ├── 📄concepts.js
👉                          ├── 📄engine.js
                            ├── 📄judge_ctrl.js
                            ├── 📄position.js
                            ├── 📄things.js
                            └── 📄user_ctrl.js
```

```js
/**
 * 思考エンジン
 */
class Engine {
    /**
     * 生成
     * @param {string} myTurn - 自分の手番。 "X" か "O"。 部屋に入ると変えることができない
     * @param {UserCtrl} userCtrl - ユーザーコントロール
     * @param {JudgeCtrl} judgeCtrl - 審判コントロール
     */
    constructor(myTurn, userCtrl, judgeCtrl) {
        console.log(`[Engine constructor] 自分の手番=${myTurn}`);

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

        // 局面
        this._position = new Position(myTurn);

        // ゲームオーバー集合
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // ユーザーコントロール
        this._userCtrl = userCtrl;

        // 審判コントロール
        this._judgeCtrl = judgeCtrl;
    }

    /**
     * 局面
     */
    get position() {
        return this._position;
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
     * ゲームオーバー集合
     */
    get gameoverSet() {
        return this._gameoverSet;
    }

    set gameoverSet(value) {
        this._gameoverSet = value;
    }

    /**
     * 対局開始時
     */
    start() {
        console.log(`[Engine start] 自分の手番=${this._position.turn.me}`);

        // 勝者のクリアー
        this._winner = "";

        // ゲームオーバー状態のクリアー
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // 局面の初期化
        this._position = new Position(this._position.turn.me);
    }

    /**
     * コマンドの実行
     */
    execute(command) {
        let log = "";

        const lines = command.split(/\r?\n/);
        for (const line of lines) {
            // 空行はパス
            if (line.trim() === "") {
                continue;
            }

            // One line command
            log += "# " + line + "\n";

            const tokens = line.split(" ");
            switch (tokens[0]) {
                case "board":
                    {
                        // Example: `board`
                        log += this._position.toBoardString();
                    }
                    break;

                case "judge":
                    {
                        // Example: `judge`
                        const gameoverSet = this._judgeCtrl.doJudge(this._position);
                        log += gameoverSet.toString();
                    }
                    break;

                case "play":
                    {
                        // Example: `play X 2`
                        const isOk = this._userCtrl.doMove(this._position, tokens[1], parseInt(tokens[2]));
                        if (isOk) {
                            log += "=\n.\n";
                        } else {
                            log += "? this engine couldn't play\n.\n";
                        }
                    }
                    break;

                case "position":
                    {
                        // Example: `position ..O.X.... next X moves 53`
                        //           -------- --------- ---- - ----- --
                        //           0        1         2    3 4     5
                        // 1. 初期局面
                        // 2. 次の番，手番
                        // 3. 初期局面からの棋譜
                        this._position.board.parse(tokens[1]);
                        this._position.turn.next = tokens[3];

                        // 棋譜の配列を作る
                        const arr = tokens[5].split("");
                        // 指定局面から指す，棋譜作成
                        this._position.record.clear();
                        for (const sq of arr) {
                            this._userCtrl.doMove(this._position, this._position.turn.next, sq);
                        }
                        log += `=\n.\n`;
                    }
                    break;

                case "undo":
                    {
                        // Example: `undo`
                        const isOk = this._userCtrl.undoMove(this._position);
                        if (isOk) {
                            log += "=\n.\n";
                        } else {
                            log += "? this engine couldn't undo\n.\n";
                        }
                    }
                    break;

                default:
                    // ignored
                    break;
            }
        }

        return log;
    }

    dump(indent) {
        return `
${indent}Engine
${indent}------
${indent}_winner:${this._winner}
${indent}${this._gameoverSet.dump(indent + "    ")}
${indent}${this._position.dump(indent + "    ")}`;
    }
}
```

# Step 8. エンジン テスト ページ作成 - engine_manual.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                ├── 📂static
                │   └── 📂tic_tac_toe
                │       └── 📂v2o0o1
                │           ├── 📄concepts.js
                │           ├── 📄engine.js
                │           ├── 📄judge_ctrl.js
                │           ├── 📄position.js
                │           ├── 📄things.js
                │           └── 📄user_ctrl.js
                └── 📂templates
                    └── 📂tic_tac_toe       # アプリケーション フォルダーと同じ名前
                        └── 📂v2o0o1
👉                          └── 📄engine_manual.html
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
        <style>
            /* 等幅 */
            .v-textarea textarea {
                font-family: monospace, monospace;
            }
        </style>
    </head>
    <body>
        <div id="app">
            <v-app>
                <v-main>
                    <v-container fluid>
                        <h1>Tic Tac Toe Engine Test</h1>
                        <v-form method="POST">
                            {% csrf_token %}

                            <!-- `po_` は POST送信するパラメーター名の目印 -->
                            <!-- 入力 -->
                            <v-textarea name="po_input" required v-model="inputText.value" label="Input"></v-textarea>

                            <v-btn block elevation="2" v-on:click="executeVu()"> Execute </v-btn>

                            <!-- 出力 -->
                            <v-textarea name="po_output" required v-model="outputText.value" label="Output"></v-textarea>
                        </v-form>
                    </v-container>
                </v-main>
            </v-app>
        </div>

        <script src="{% static 'tic_tac_toe/v2o0o1/things.js' %}"></script>
        <script src="{% static 'tic_tac_toe/v2o0o1/concepts.js' %}"></script>
        <script src="{% static 'tic_tac_toe/v2o0o1/position.js' %}"></script>
        <script src="{% static 'tic_tac_toe/v2o0o1/user_ctrl.js' %}"></script>
        <script src="{% static 'tic_tac_toe/v2o0o1/judge_ctrl.js' %}"></script>
        <script src="{% static 'tic_tac_toe/v2o0o1/engine.js' %}"></script>
        <!--                    ============================
                                1
        1. host1/apps1/tic_tac_toe/static/tic-ta-toe/v2o0o1/engine.js
                                          ===========================
        -->

        <script src="https://cdn.jsdelivr.net/npm/vue@2.x/dist/vue.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
        <script>
            const vue1 = new Vue({
                el: "#app",
                vuetify: new Vuetify(),
                data: {
                    // 入力
                    inputText: {
                        value: `board
judge
play X 1
board
judge
play O 4
board
judge
play X 5
board
judge
play O 2
board
judge
play X 6
board
judge
play O 0
board
judge
play X 8
board
judge
play O 7
board
judge
play X 3
board
judge

position ..O.X.... next X moves 53
board
undo
board
undo
board
undo
board
`,
                    },
                    // 出力
                    outputText: {
                        value: 'Please push "Execute" button.',
                    },
                    // 思考エンジン
                    engine: new Engine(
                        // 自分の番。 とりあえず "X" としておく
                        PC_X_LABEL,
                        // ユーザーコントロール
                        new UserCtrl(
                            /**
                             * onDidMove - 駒を置いたあと
                             *
                             * * 手番がひっくり返っていることに注意してください
                             *
                             * @param {int} sq - マス番号
                             * @param {string} pieceMoved - 動かした駒
                             */
                            (sq, pieceMoved) => {
                                console.log(`[Engine onDidMove] 置いたマス=${sq} 動かした駒=${pieceMoved}`);
                            }
                        ),
                        // 審判コントロール
                        new JudgeCtrl(
                            /**
                             * onDoJudge - 判断したとき
                             *
                             * @param {*} gameoverSet - ゲームオーバー集合
                             */
                            (gameoverSet) => {
                                console.log(`[Engine onDoJudge] 自分の番=${vue1.engine.position.turn.me}`);
                                vue1.engine.gameoverSet = gameoverSet;

                                switch (gameoverSet.value) {
                                    case GameoverSet.won:
                                        // 勝ったとき
                                        console.log(`[Engine onDoJudge] 勝ち`);
                                        break;
                                    case GameoverSet.draw:
                                        // 引き分けたとき
                                        console.log(`[Engine onDoJudge] 引き分け`);
                                        break;
                                    case GameoverSet.lost:
                                        // 負けたとき
                                        console.log(`[Engine onDoJudge] 負け`);
                                        break;
                                    case GameoverSet.none:
                                        // なんでもなかったとき
                                        console.log(`[Engine onDoJudge] 何もなし`);
                                        break;
                                    default:
                                        throw new Error(`Unexpected gameoverSet.value=${gameoverSet.value}`);
                                }
                            }
                        )
                    ),
                },
                methods: {
                    // 関数名の末尾の Vu は vue1 のメソッドであることを表す目印
                    /**
                     * po_input 欄のコマンドを入力します
                     */
                    executeVu() {
                        console.log(`[methods executeVu]`);
                        vue1.outputText.value = vue1.engine.execute(vue1.inputText.value);
                    },
                },
            });
        </script>
    </body>
</html>
```

# Step 9. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂apps1
            └── 📂tic_tac_toe               # アプリケーション フォルダー
                ├── 📂static
                │   └── 📂tic_tac_toe
                │       └── 📂v2o0o1
                │           ├── 📄concepts.js
                │           ├── 📄engine.js
                │           ├── 📄judge_ctrl.js
                │           ├── 📄position.js
                │           ├── 📄things.js
                │           └── 📄user_ctrl.js
                ├── 📂templates
                │   └── 📂tic_tac_toe
                │       └── 📂v2o0o1
                │           └── 📄engine_manual.html
                └── 📂views
                    └── 📂tic_tac_toe
                        └── 📂v2o0o1
👉                          └── 📄resources.py
```

```py
"""〇×ゲームの練習２．０．１"""
from django.shortcuts import render


class EngineManual():
    """エンジン手動"""

    _path_of_html = "tic_tac_toe/v2o0o1/engine_manual.html"
    #                             ^^^^^ two o zero o one
    #                -------------------------------------
    #                1
    # 1. host1/apps1/tic_tac_toe/templates/tic_tac_toe/v2o0o1/engine_manual.html
    #                                      -------------------------------------

    @staticmethod
    def render(request):
        """描画"""
        return render_match_application(request, EngineManual._path_of_html)


# 以下、関数


def render_match_application(request, path_of_html):
    """対局申込 - 描画"""

    context = {}

    return render(request, path_of_html, context)
```

# Step 10. ルート編集 - urls.py ファイル

以下の既存のファイルに、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v2o0o1
        │       │           ├── 📄concepts.js
        │       │           ├── 📄engine.js
        │       │           ├── 📄judge_ctrl.js
        │       │           ├── 📄position.js
        │       │           ├── 📄things.js
        │       │           └── 📄user_ctrl.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v2o0o1
        │       │           └── 📄engine_manual.html
        │       ├── 📂views
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v2o0o1
        │       │           └── 📄resources.py
👉      │       └── 📄urls.py                   # こちら
❌      └── 📄urls.py                           # これではない
```

```py
from django.urls import path


# ...中略...


# 〇×ゲームの練習２．０．１
from apps1.tic_tac_toe.views.v2o0o1 import resources as tic_tac_toe_v2o0o1
#    ----- ----------- ------------        ---------    ------------------
#    1     2           3                   4            5
#    ------------------------------
#    6
# 1. 開発者用ディレクトリーの一部
# 2. アプリケーション フォルダー名
# 3. ディレクトリー名
# 4. Python ファイル名。拡張子抜き
# 5. `4.` の別名
# 6. モジュール名


# ...略...


urlpatterns = [


    # ...略...


    # +----
    # | 〇×ゲーム２．０．１

    # 対局申込
    path('tic-tac-toe/v2o0o1/engine-manual/',
         #             ^^^^^ two o zero o one
         # --------------------------------
         # 1
         tic_tac_toe_v2o0o1.EngineManual.render),
    #                 ^^^^^ two o zero o one
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v2o0o1/engine-manual/` のような URL のパスの部分
    #                              ---------------------------------
    # 2. tic_tac_toe_v2o0o1 (別名)ファイルの EngineManual クラスの render 静的メソッド

    # | 〇×ゲーム２．０．１
    # +----
]
```

# Step 11. Web画面へアクセス

📖 [http://localhost:8000/tic-tac-toe/v2o0o1/engine-manual/](http://localhost:8000/tic-tac-toe/v2o0o1/engine-manual/)  

# 次の記事

📖 [Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！ Vuetify編](https://qiita.com/muzudho1/items/f302bdb40fb5c13f9603)  

# 参考にした記事

## Java Script

📖 [【JavaScript】配列を複製する](https://zenn.dev/kou_pg_0131/articles/js-clone-array) - スプレッド構文  
📖 [Split a String by Newline in JavaScript](https://bobbyhadz.com/blog/javascript-split-string-by-newline#split-a-string-by-newline-in-javascript) - 改行でスプリット  
