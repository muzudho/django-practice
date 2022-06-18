/**
 * 局面
 */
class Position {
    /**
     * 初期化
     *
     * * 対局開始時
     *
     * @param {string} myPiece - "X", "O", "_"
     */
    constructor(myPiece) {
        console.log(`[Position constructor] myPiece=${myPiece} PC_EMPTY=${PC_EMPTY} PC_X_LABEL=${PC_X_LABEL}`);

        // 盤面
        this._board = new Board();

        // 棋譜
        this._record = new Record();

        // 自分の手番
        this._myTurn = new MyTurn(myPiece);
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
     * ダンプ
     */
    dump(indent) {
        return `
${indent}Position
${indent}--------
${indent}${this._board.dump(indent + "    ")}
${indent}${this._record.dump(indent + "    ")}
${indent}${this._myTurn.dump(indent + "    ")}`;
    }
}
