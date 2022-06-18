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
     * @param {function} onChangeValue - 値の変更時
     */
    constructor(value, onChangeValue) {
        console.log(`[RoomState constructor]`);

        this._value = value;
        this._onChangeValue = onChangeValue;
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
        this._onChangeValue(oldValue, this._value);
    }

    /**
     * ダンプ
     * @param {str} indent
     * @returns
     */
    dump(indent) {
        return `
${indent}RoomState
${indent}---------
${indent}_value:${this._value}`;
    }
}

/**
 * 番
 */
class Turn {
    /**
     * 生成
     * @param {*} myTurn - 自分の手番。 "X", "O"
     */
    constructor(myTurn) {
        // 自分の手番
        this._me = myTurn;

        // 自分の手番か（初回はXが先手）
        this._isMe = this._me == PC_X_LABEL;
    }

    /**
     * 自分の手番
     */
    get me() {
        return this._me;
    }

    /**
     * 私の番か？
     */
    get isMe() {
        return this._isMe;
    }

    set isMe(value) {
        this._isMe = value;
        vue1.raiseMyTurnChanged();
    }

    /**
     * ダンプ
     * @param {str} indent
     * @returns
     */
    dump(indent) {
        return `
${indent}Turn
${indent}----
${indent}_me:${this._me}
${indent}_isMe:${this._isMe}`;
    }
}

/**
 * ゲームオーバー集合
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

    /**
     * ダンプ
     * @param {str} indent
     * @returns
     */
    dump(indent) {
        let text;
        switch (this._value) {
            case GameoverSet.none:
                text = "none";
                break;
            case GameoverSet.win:
                text = "win";
                break;
            case GameoverSet.draw:
                text = "draw";
                break;
            case GameoverSet.lose:
                text = "lose";
                break;
            default:
                throw Error(`[GameoverSet dump] Unexpected value=${this._value}`);
        }

        return `
${indent}GameoverSet
${indent}-----------
${indent}_value:${text}`;
    }
}

/**
 * 駒が３つ並んでいるパターン
 */
WIN_PATTERN = [
    // +---------+
    // | *  *  * |
    // | .  .  . |
    // | .  .  . |
    // +---------+
    [SQ_0, SQ_1, SQ_2],
    // +---------+
    // | .  .  . |
    // | *  *  * |
    // | .  .  . |
    // +---------+
    [SQ_3, SQ_4, SQ_5],
    // +---------+
    // | .  .  . |
    // | .  .  . |
    // | *  *  * |
    // +---------+
    [SQ_6, SQ_7, SQ_8],
    // +---------+
    // | *  .  . |
    // | *  .  . |
    // | *  .  . |
    // +---------+
    [SQ_0, SQ_3, SQ_6],
    // +---------+
    // | .  *  . |
    // | .  *  . |
    // | .  *  . |
    // +---------+
    [SQ_1, SQ_4, SQ_7],
    // +---------+
    // | .  .  * |
    // | .  .  * |
    // | .  .  * |
    // +---------+
    [SQ_2, SQ_5, SQ_8],
    // +---------+
    // | *  .  . |
    // | .  *  . |
    // | .  .  * |
    // +---------+
    [SQ_0, SQ_4, SQ_8],
    // +---------+
    // | .  .  * |
    // | .  *  . |
    // | *  .  . |
    // +---------+
    [SQ_2, SQ_4, SQ_6],
];

/**
 * 手番反転
 *
 * @param {*} piece
 * @returns
 */
function flipTurn(piece) {
    if (piece == PC_X_LABEL) {
        return PC_O_LABEL;
    } else if (piece == PC_O_LABEL) {
        return PC_X_LABEL;
    }

    return piece;
}
