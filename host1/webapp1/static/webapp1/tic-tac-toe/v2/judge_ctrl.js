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
        this._playeq.gameoverState.value = this.#makeGameoverSet();
        console.log(`[doJudge] gameoverState=${this._playeq.gameoverState.value}`);

        switch (this._playeq.gameoverState.value) {
            case GameoverSet.win:
                this._onWon(myPiece);
                break;
            case GameoverSet.draw:
                this._onDraw();
                break;
            case GameoverSet.lose: // thru
            case GameoverSet.none:
                break;
            default:
                throw new Error(`Unexpected gameoverState=${this._playeq.gameoverState.value}`);
        }
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
            for (let squaresOfWinPattern of WIN_PATTERN) {
                console.log(`[#makeGameoverSet] this.#isPieceInLine(squaresOfWinPattern)=${this.#isPieceInLine(squaresOfWinPattern)}`);
                if (this.#isPieceInLine(squaresOfWinPattern)) {
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
     * 石が３つ並んでいるか？
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
