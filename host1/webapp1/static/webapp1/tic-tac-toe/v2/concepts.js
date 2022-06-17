/**
 * 自分のターン
 */
class MyTurn {
    /**
     *
     * @param {*} myPiece - 自分の駒。 "X", "O", "_"
     */
    constructor(myPiece) {
        // 自分の手番か（初回は先手）
        this._isTrue = myPiece == PC_X_LABEL;
    }

    /**
     * 真実か？
     */
    get isTrue() {
        return this._isTrue;
    }

    set isTrue(value) {
        this._isTrue = value;
        vue1.raiseMyTurnChanged();
    }
}
