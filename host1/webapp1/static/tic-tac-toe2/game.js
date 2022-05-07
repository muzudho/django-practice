/**
 * PC は Piece （駒、石、などの意味）の略です。
 * @type {number}
 */
const PC_EMPTY = -1 // Pieceがないことを表します
const PC_O = 0
const PC_X = 1

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
        // 初期化
        this.reset()

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
     * 初期化
     */
    reset() {
        // 盤面
        this.board = [
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
        ];

        this.countOfMove = 0;   // 何手目
        this.myTurn = true;     // 自分の手番か
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

        if(this.myTurn){
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
