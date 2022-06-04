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
     * ゲームオーバー判定
     */
    doJudge(myPiece) {
        this._playeq.gameoverState = this.#makeGameoverState();
        console.log(`[doJudge] gameoverState=${this._playeq.gameoverState}`);

        switch (this._playeq.gameoverState) {
            case GAMEOVER_WIN:
                this._onWon(myPiece);
                break;
            case GAMEOVER_DRAW:
                this._onDraw();
                break;
            case GAMEOVER_LOSE:
                break;
            case GAMEOVER_NONE:
                break;
            default:
                throw new Error(`Unexpected gameoverState=${this._playeq.gameoverState}`);
        }
    }

    /**
     * ゲームオーバー判定
     *
     * * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください
     *
     * @returns ゲームオーバー状態
     */
    #makeGameoverState() {
        console.log(`[#makeGameoverState] isThere3SamePieces=${this._playeq.isThere3SamePieces()}`);
        if (this._playeq.isThere3SamePieces()) {
            for (let squaresOfWinPattern of WIN_PATTERN) {
                console.log(`[#makeGameoverState] this.#isPieceInLine(squaresOfWinPattern)=${this.#isPieceInLine(squaresOfWinPattern)}`);
                if (this.#isPieceInLine(squaresOfWinPattern)) {
                    console.log(`[#makeGameoverState] this._playeq.isMyTurn=${this._playeq.isMyTurn}`);
                    if (this._playeq.isMyTurn) {
                        // 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return GAMEOVER_LOSE;
                    } else {
                        // 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return GAMEOVER_WIN;
                    }
                }
            }
        }

        // 勝ち負けが付かず、盤が埋まったら引き分け
        if (this._playeq.isBoardFill()) {
            return GAMEOVER_DRAW;
        }

        // ゲームオーバーしてません
        return GAMEOVER_NONE;
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
