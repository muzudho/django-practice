/**
 * 遊具
 */
class PlaygroundEquipment {
    constructor() {
        // あとで onStart(...) を呼出してください
    }

    /**
     * 対局開始時
     */
    onStart(myPiece) {
        // 盤面
        this._board = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];

        // 何手目
        this._countOfMove = 0;

        // 自分の手番か
        this._isMyTurn = myPiece == PC_X_LABEL;

        // 「相手の手番に着手しないでください」というアラートの可視性
        this._isVisibleAlertWaitForOther = false;

        // ゲームオーバーしてません
        this._gameoverState = GAMEOVER_NONE;

        // イベントハンドラはそのまま
    }

    /**
     * 盤上のマス番号で示して、駒を取得
     * @param {number} sq - マス番号
     */
    getPieceBySq(sq) {
        return this._board[sq];
    }

    /**
     * 盤上のマスに駒を上書きします
     *
     * @param {*} sq - マス番号
     * @param {*} piece - 駒
     */
    setPiece(sq, piece) {
        this._board[sq] = piece;
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
