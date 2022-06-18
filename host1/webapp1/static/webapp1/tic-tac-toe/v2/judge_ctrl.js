/**
 * 審判コントロール
 */
class JudgeCtrl {
    /**
     * 初期化
     */
    constructor() {
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
     *
     * * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください
     *
     * @param {Position} position - 局面
     */
    doJudge(position, piece_moved) {
        let gameoverSetValue = this.#makeGameoverSetValue(position);
        console.log(`[doJudge] gameoverSetValue=${gameoverSetValue}`);
        this._onJudged(piece_moved, gameoverSetValue);
    }

    /**
     * ゲームオーバー判定
     *
     * @param {Position} position - 局面
     * @returns ゲームオーバー元
     */
    #makeGameoverSetValue(position) {
        if (position.isThere3SamePieces()) {
            // 先手番が駒を３つ置いてから、判定を始めます
            for (let squaresOfWinPattern of WIN_PATTERN) {
                // 勝ちパターンの１つについて
                if (this.#isPieceInLine(position, squaresOfWinPattern)) {
                    // 当てはまるなら
                    if (position.turn.isMe) {
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
        if (position.isBoardFill()) {
            return GameoverSet.draw;
        }

        // ゲームオーバーしてません
        return GameoverSet.none;
    }

    /**
     * 駒が３つ並んでいるか？
     *
     * @param {Position} position - 局面
     * @param {*} squaresOfWinPattern - 勝ちパターン
     * @returns 並んでいれば真、それ以外は偽
     */
    #isPieceInLine(position, squaresOfWinPattern) {
        return (
            position.board.getPieceBySq(squaresOfWinPattern[0]) !== PC_EMPTY && //
            position.board.getPieceBySq(squaresOfWinPattern[0]) === position.board.getPieceBySq(squaresOfWinPattern[1]) &&
            position.board.getPieceBySq(squaresOfWinPattern[0]) === position.board.getPieceBySq(squaresOfWinPattern[2])
        );
    }
}
