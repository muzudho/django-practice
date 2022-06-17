/**
 * ユーザーコントロール
 */
class UserCtrl {
    /**
     *
     * @param {*} playeq - 遊具
     */
    constructor(playeq) {
        // 遊具
        this._playeq = playeq;

        // イベントリスナー
        this._onDoMove = () => {};
    }

    /**
     * 石を置いたとき
     */
    set onDoMove(func) {
        this._onDoMove = func;
    }

    /**
     * 石を置きます
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} piece - X か O
     * @returns 石を置けたら真、それ以外は偽
     */
    doMove(sq, piece) {
        if (this._playeq.gameoverState.value != GameoverSet.none) {
            // イリーガルムーブなら何もしません
            console.log(`warning of illegal move. gameoverState=${this._playeq.gameoverState.value}`);
        }

        if (this._playeq.board.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら駒を置きます

            this._playeq.record.push(sq); // 棋譜に追加

            // 石を置きます
            switch (piece) {
                case PC_X_LABEL:
                    this._playeq.board.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    this._playeq.board.setPiece(sq, PC_O);
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
