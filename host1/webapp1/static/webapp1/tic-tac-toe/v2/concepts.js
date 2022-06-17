/**
 * 部屋の状態
 */
class RoomState {
    /**
     * ゲームしてません
     */
    static get none() {
        return 0;
    }

    /**
     * ゲーム中
     */
    static get playing() {
        return 1;
    }

    /**
     * 生成
     * @param {int} value
     * @param {function} changeValue - 値の変更
     */
    constructor(value, changeValue) {
        console.log(`[RoomState constructor]`);

        this._value = value;
        this._changeValue = changeValue;
    }

    /**
     * 値
     */
    get value() {
        return this._value;
    }

    set value(value) {
        console.log(`[RoomState set value]`);

        if (this._value === value) {
            return;
        }

        let oldValue = this._value;
        this._value = value;
        this._changeValue(oldValue, this._value);
    }
}

/**
 * 自分のターン
 */
class MyTurn {
    /**
     * 生成
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

    /**
     * 生成
     * @param {int} value
     */
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
