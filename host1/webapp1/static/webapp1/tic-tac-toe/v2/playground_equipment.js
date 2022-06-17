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
        console.log(`[PlaygroundEquipment onStart] myPiece=${myPiece} PC_EMPTY=${PC_EMPTY} PC_X_LABEL=${PC_X_LABEL} GAMEOVER_NONE=${GAMEOVER_NONE}`);

        // 盤面
        this._board = new Board();

        // 何手目
        this._countOfMove = 0;

        // 自分の手番か（初回は先手）
        this._isMyTurn = myPiece == PC_X_LABEL;

        // 「相手の手番に着手しないでください」というアラートの可視性
        this._isVisibleAlertWaitForOther = false;

        // ゲームオーバーしてません
        this._gameoverState = GAMEOVER_NONE;
    }

    /**
     * 盤
     */
    get board() {
        return this._board;
    }

    /**
     * 手数を１増やします
     */
    incrementCountOfMove() {
        this._countOfMove++;
    }

    /**
     * マスがすべて埋まっていますか
     */
    isBoardFill() {
        return this._countOfMove == 9;
    }

    /**
     * 同じ駒が３個ありますか
     */
    isThere3SamePieces() {
        return 5 <= this._countOfMove;
    }

    /**
     * 私のターンですか
     */
    get isMyTurn() {
        return this._isMyTurn;
    }

    set isMyTurn(value) {
        this._isMyTurn = value;
        vue1.raiseMyTurnChanged();
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

    /**
     * ゲームオーバー状態
     */
    get gameoverState() {
        return this._gameoverState;
    }

    set gameoverState(value) {
        this._gameoverState = value;
    }
}
