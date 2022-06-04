/**
 * 審判コントロール
 */
class JudgeCtrl {
    constructor(userCtrl) {
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
            else if (!gameOver && this._userCtrl.countOfMove == 9) {
                this._onDraw();
            }
        }
    }

    /**
     * 手番を持っている方が勝っているか？
     * @returns 勝ちなら真、それ以外は偽
     */
    #isGameOver() {
        if (5 <= this._userCtrl.countOfMove) {
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
            this._userCtrl.playeq.getPieceBySq(squaresOfWinPattern[0]) !== PC_EMPTY && //
            this._userCtrl.playeq.getPieceBySq(squaresOfWinPattern[0]) === this._userCtrl.playeq.getPieceBySq(squaresOfWinPattern[1]) &&
            this._userCtrl.playeq.getPieceBySq(squaresOfWinPattern[0]) === this._userCtrl.playeq.getPieceBySq(squaresOfWinPattern[2])
        );
    }
}
