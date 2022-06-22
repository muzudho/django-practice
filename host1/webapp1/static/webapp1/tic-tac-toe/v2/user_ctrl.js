/**
 * ユーザーコントロール
 */
class UserCtrl {
    /**
     * 初期化
     *
     * @param {function} onDidMove - 駒を置いたあと
     */
    constructor(onDidMove) {
        this._onDidMove = onDidMove;
    }

    /**
     * 駒を置きます
     *
     * @param {Position} position - 局面
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} piece - X か O
     * @returns 駒を置けたら真、それ以外は偽
     */
    doMove(position, piece, sq) {
        if (position.board.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら駒を置きます
            console.log(`[UserCtrl doMove] 置いたマス:${sq} 動かした駒:${piece}`);

            position.record.push(sq); // 棋譜に追加

            // 駒を置きます
            switch (piece) {
                case PC_X_LABEL:
                    position.board.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    position.board.setPiece(sq, PC_O);
                    break;
                default:
                    console.log(`[UserCtrl doMove] illegal move. invalid piece:${piece}`);
                    return false;
            }

            console.log(`[UserCtrl doMove] 反転前の手番=${position.turn.next}`);
            position.turn.next = flipTurn(position.turn.next);
            console.log(`[UserCtrl doMove] 反転後の手番=${position.turn.next}`);

            this._onDidMove(sq, piece);
            return true;
        }

        // 駒が置いてあるマスに駒は置けません
        console.log(`[UserCtrl doMove] illegal move. not empty square. sq:${sq}`);
        return false;
    }

    /**
     * 一手戻します
     *
     * @param {Position} position - 局面
     * @returns {bool} wasItDelete - 削除しました
     */
    undoMove(position) {
        const previousSq = position.record.pop();
        console.log(`[UserCtrl undoMove] previousSq:${previousSq}`);

        if (typeof previousSq === "undefined") {
            return false;
        }

        console.log(`[UserCtrl doMove] 反転前の手番:${position.turn.next}`);
        position.turn.next = flipTurn(position.turn.next);
        console.log(`[UserCtrl doMove] 反転後の手番:${position.turn.next}`);

        // 盤上の駒を消します
        position.board.setPiece(previousSq, PC_EMPTY);
        return true;
    }
}
