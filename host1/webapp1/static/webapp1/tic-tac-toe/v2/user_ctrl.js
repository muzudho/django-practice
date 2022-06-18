/**
 * ユーザーコントロール
 */
class UserCtrl {
    /**
     * 初期化
     *
     * @param {function} onDoMove - 駒を置いたとき
     */
    constructor(onDoMove) {
        this._onDoMove = onDoMove;
    }

    /**
     * 駒を置きます
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} piece - X か O
     * @returns 駒を置けたら真、それ以外は偽
     */
    doMove(position, piece, sq) {
        if (position.board.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら駒を置きます

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
                    alert(`[Error] Invalid piece = ${piece}`);
                    return false;
            }

            console.log(`[UserCtrl doMove] sq=${sq} piece=${piece}`);
            this._onDoMove(sq, piece);
        }

        return true;
    }
}
