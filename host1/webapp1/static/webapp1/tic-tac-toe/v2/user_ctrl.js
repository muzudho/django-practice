/**
 * ユーザーコントロール
 */
class UserCtrl {
    constructor() {
        // 遊具
        this._playeq = new PlaygroundEquipment();

        this.clear();

        // イベントリスナー
        this._onDoMove = () => {};
    }

    /**
     * 遊具
     */
    get playeq() {
        return this._playeq;
    }

    /**
     * 石を置いたとき
     */
    set onDoMove(func) {
        this._onDoMove = func;
    }

    /**
     * クリアー
     */
    clear() {
        // console.log(`[Debug][UserCtrl#clear] Begin this.isMyTurn=${this.isMyTurn}`);

        // 遊具
        this._playeq.clear();

        // 何手目
        this.countOfMove = 0;

        // 自分の手番ではない
        this.isMyTurn = false;

        // 相手の手番に着手しないでください
        this.isWaitForOther = false;

        // console.log(`[Debug][UserCtrl#clear] End this.isMyTurn=${this.isMyTurn}`);
    }

    /**
     * 初期化
     */
    init(myPiece) {
        this.clear();

        // 自分の手番か
        {
            let isMyTurn;

            // console.log(`[Debug][UserCtrl#init] myPiece=${myPiece} PC_X_LABEL=${PC_X_LABEL}`);

            if (myPiece == PC_X_LABEL) {
                isMyTurn = true;
            } else {
                isMyTurn = false;
            }
            this.isMyTurn = isMyTurn;
        }

        // イベントハンドラはそのまま
    }

    /**
     * 石を置きます
     * @param {number} sq - 升番号; 0 <= sq
     * @param {*} myPiece - X か O
     * @returns 石を置けたら真、それ以外は偽
     */
    doMove(sq, myPiece) {
        if (this.playeq.getPieceBySq(sq) == PC_EMPTY) {
            // 空升なら

            this.countOfMove++; // 何手目を＋１

            // 石を置きます
            switch (myPiece) {
                case PC_X_LABEL:
                    this.playeq.setPiece(sq, PC_X);
                    break;
                case PC_O_LABEL:
                    this.playeq.setPiece(sq, PC_O);
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
