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
 * ゲーム
 */
class Game {
    constructor() {
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
        // console.log(`[Debug][Game#clear] Begin this.isMyTurn=${this.isMyTurn}`);

        // 盤面
        this.board = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];

        // 何手目
        this.countOfMove = 0;

        // 自分の手番ではない
        this.isMyTurn = false;

        // 相手の手番に着手しないでください
        this.isWaitForOther = false;

        // console.log(`[Debug][Game#clear] End this.isMyTurn=${this.isMyTurn}`);
    }

    /**
     * 初期化
     */
    init(myPiece) {
        this.clear();

        // 自分の手番か
        {
            let isMyTurn;

            // console.log(`[Debug][Game#init] myPiece=${myPiece} PC_X_LABEL=${PC_X_LABEL}`);

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
    makeMove(sq, myPiece) {
        if (this.board[sq] == PC_EMPTY) {
            // 空升なら

            this.countOfMove++; // 何手目を＋１

            // 石を置きます
            switch (myPiece) {
                case PC_X_LABEL:
                    this.board[sq] = PC_X;
                    break;
                case PC_O_LABEL:
                    this.board[sq] = PC_O;
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
