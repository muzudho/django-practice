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
     * @param {*} myPiece - X か O
     * @returns 石を置けたら真、それ以外は偽
     */
    doMove(sq, myPiece) {
        if (this._playeq.gameoverState != GAMEOVER_NONE) {
            // Warning of illegal move
            console.log(`Warning of illegal move. gameoverState=${this._playeq.gameoverState}`);
        }

        if (this._playeq.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら

            this._playeq.incrementCountOfMove(); // 手数を１増やします

            // 石を置きます
            switch (myPiece) {
                case PC_X_LABEL:
                    this._playeq.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    this._playeq.setPiece(sq, PC_O);
                    break;
                default:
                    alert(`[Error] Invalid my piece = ${myPiece}`);
                    return false;
            }

            this._onDoMove(sq, myPiece);
        }

        return true;
    }
}
