/**
 * 審判コントロール
 */
class JudgeCtrl {
    /**
     *
     * @param {*} position - 局面
     * @param {*} userCtrl - ユーザーコントロール
     */
    constructor(position, userCtrl) {
        // 局面
        this._position = position;

        // ユーザーコントロール
        this._userCtrl = userCtrl;

        // 判断したとき
        this._onJudged = (pieceMoved, gameoverSetValue) => {};
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
        let gameoverSetValue = this.#makeGameoverSetValue();
        console.log(`[doJudge] gameoverSetValue=${gameoverSetValue}`);
        this._onJudged(piece_moved, gameoverSetValue);
    }

    /**
     * ゲームオーバー判定
     *
     * * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください
     *
     * @returns ゲームオーバー状態
     */
    #makeGameoverSetValue() {
        console.log(`[#makeGameoverSetValue] isThere3SamePieces=${this._position.isThere3SamePieces()}`);
        if (this._position.isThere3SamePieces()) {
            // 先手番が駒を３つ置いてから、判定を始めます
            for (let squaresOfWinPattern of WIN_PATTERN) {
                // 勝ちパターンの１つについて
                console.log(`[#makeGameoverSetValue] this.#isPieceInLine(squaresOfWinPattern)=${this.#isPieceInLine(squaresOfWinPattern)}`);
                if (this.#isPieceInLine(squaresOfWinPattern)) {
                    // 当てはまるなら
                    console.log(`[#makeGameoverSetValue] this._position.myTurn.isTrue=${this._position.myTurn.isTrue}`);
                    if (this._position.myTurn.isTrue) {
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
        if (this._position.isBoardFill()) {
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
            this._position.board.getPieceBySq(squaresOfWinPattern[0]) !== PC_EMPTY && //
            this._position.board.getPieceBySq(squaresOfWinPattern[0]) === this._position.board.getPieceBySq(squaresOfWinPattern[1]) &&
            this._position.board.getPieceBySq(squaresOfWinPattern[0]) === this._position.board.getPieceBySq(squaresOfWinPattern[2])
        );
    }
}
