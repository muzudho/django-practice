/**
 * 審判コントロール
 */
class JudgeCtrl {
    /**
     * 初期化
     *
     * @param {function} onJudged - 判断したとき。 (pieceMoved, gameoverSetValue) => {};
     */
    constructor(onJudged) {
        // 判断したとき
        this._onJudged = onJudged;
    }

    /**
     * ゲームオーバー判定
     *
     * * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください
     *
     * @param {Position} position - 局面
     */
    doJudge(position) {
        let gameoverSet = this.#makeGameoverSet(position);
        console.log(`[doJudge] gameoverSet.toString()=${gameoverSet.toString()}`);
        this._onJudged(gameoverSet);

        return gameoverSet;
    }

    /**
     * ゲームオーバー判定
     *
     * @param {Position} position - 局面
     * @returns ゲームオーバー元
     */
    #makeGameoverSet(position) {
        if (position.isThere3SamePieces()) {
            // 先手番が駒を３つ置いてから、判定を始めます
            for (let squaresOfWinPattern of WIN_PATTERN) {
                // 勝ちパターンの１つについて
                if (this.#isPieceInLine(position, squaresOfWinPattern)) {
                    // 当てはまるなら
                    if (position.turn.isMe) {
                        // 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return new GameoverSet(GameoverSet.lost);
                    } else {
                        // 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return new GameoverSet(GameoverSet.won);
                    }
                }
            }
        }

        // 勝ち負けが付かず、盤が埋まったら引き分け
        if (position.isBoardFill()) {
            return new GameoverSet(GameoverSet.draw);
        }

        // ゲームオーバーしてません
        return new GameoverSet(GameoverSet.none);
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
