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

/**
 * ゲームオーバー状態
 *
 * * 自分視点
 */
class GameoverSet {
    /**
     * ゲームオーバーしてません
     */
    static get none() {
        return 0;
    }

    /**
     * 勝ち
     */
    static get win() {
        return 1;
    }

    /**
     * 引き分け
     */
    static get draw() {
        return 2;
    }

    /**
     * 負け
     */
    static get lose() {
        return 3;
    }

    constructor(value) {
        this._value = value;
    }

    /**
     * 値
     */
    get value() {
        return this._value;
    }

    set value(value) {
        this._value = value;
    }
}
