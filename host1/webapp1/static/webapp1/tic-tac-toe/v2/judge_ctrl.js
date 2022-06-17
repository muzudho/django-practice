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
