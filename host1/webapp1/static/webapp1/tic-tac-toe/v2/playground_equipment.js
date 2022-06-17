/**
 * 遊具
 */
class PlaygroundEquipment {
    constructor() {
        // あとで onStart(...) を呼出してください
    }

    /**
     * 対局開始時
     *
     * @param {string} myPiece - "X", "O", "_"
     */
    onStart(myPiece) {
        console.log(`[PlaygroundEquipment onStart] myPiece=${myPiece} PC_EMPTY=${PC_EMPTY} PC_X_LABEL=${PC_X_LABEL}`);

        // 盤面
        this._board = new Board();

        // 棋譜
        this._record = new Record();

        // 自分の手番
        this._myTurn = new MyTurn(myPiece);

        // 「相手の手番に着手しないでください」というアラートの可視性
        this._isVisibleAlertWaitForOther = false;

        // ゲームオーバー状態
        this._gameoverState = new GameoverSet(GameoverSet.none);
    }

    /**
     * 盤
     */
    get board() {
        return this._board;
    }

    /**
     * 棋譜
     */
    get record() {
        return this._record;
    }

    /**
     * 自分のターン
     */
    get myTurn() {
        return this._myTurn;
    }

    /**
     * ゲームオーバー状態
     */
    get gameoverState() {
        return this._gameoverState;
    }

    /**
     * マスがすべて埋まっていますか
     */
    isBoardFill() {
        return this.record.length == 9;
    }

    /**
     * 同じ駒が３個ありますか
     */
    isThere3SamePieces() {
        return 5 <= this.record.length;
    }

    /**
     * 「相手の手番に着手しないでください」というアラートの可視性
     */
    get isVisibleAlertWaitForOther() {
        return this._isVisibleAlertWaitForOther;
    }

    set isVisibleAlertWaitForOther(value) {
        this._isVisibleAlertWaitForOther = value;
    }
}
