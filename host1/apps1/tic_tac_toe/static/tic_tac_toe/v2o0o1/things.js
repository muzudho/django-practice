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
