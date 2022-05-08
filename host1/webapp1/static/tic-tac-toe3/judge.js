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

class Judge {
    constructor(game) {
        this._game = game

        // イベントリスナー
        this._onWon = () => {}
        this._onDraw = () => {}
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
     * 勝敗判定
     */
    judge(myPiece) {
        if(this._game.isMyTurn){
            // 終局判定
            const gameOver = this.#isGameOver();

            // 打った後、負けと判定されたなら、相手が負け
            if (gameOver) {
                this._onWon(myPiece)
            }
            // 盤が埋まったら引き分け
            else if (!gameOver && this._game.countOfMove == 9) {
                this._onDraw()
            }
        }
    }

    /**
     * 手番を持っている方が勝っているか？
     * @returns 勝ちなら真、それ以外は偽
     */
    #isGameOver(){
        if (5 <= this._game.countOfMove) {
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
        return this._game.board[squaresOfWinPattern[0]] !== PC_EMPTY &&
            this._game.board[squaresOfWinPattern[0]] === this._game.board[squaresOfWinPattern[1]] &&
            this._game.board[squaresOfWinPattern[0]] === this._game.board[squaresOfWinPattern[2]];
    }
}