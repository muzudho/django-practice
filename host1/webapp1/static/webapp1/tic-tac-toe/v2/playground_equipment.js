/**
 * 遊具
 */
class PlaygroundEquipment {
    constructor() {
        this.clear();
    }

    /**
     * クリアー
     */
    clear() {
        // 盤面
        this._board = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];

        // 何手目
        this._countOfMove = 0;
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
}
