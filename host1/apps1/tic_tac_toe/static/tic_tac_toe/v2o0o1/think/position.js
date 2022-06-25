/**
 * 局面
 */
class Position {
    /**
     * 初期化
     *
     * * 対局開始時
     *
     * @param {string} myTurn - 自分の手番。 "X", "O"
     */
    constructor(myTurn) {
        console.log(`[Position constructor] 自分の手番=${myTurn}`);

        // 盤面
        this._board = new Board();

        // 棋譜
        this._record = new Record();

        // 番
        this._turn = new Turn(myTurn);
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
     * 番
     */
    get turn() {
        return this._turn;
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

    toBoardString() {
        // 何手目
        const moves = this._record.length + 1;

        // 手番
        let currentTurn;
        if (this._turn.isMe) {
            currentTurn = this._turn.me;
        } else {
            currentTurn = flipTurn(this._turn.me);
        }

        // 各マス
        const squares = this._board.toArray();
        console.log(`squares=${squares}`);
        const [a, b, c, d, e, f, g, h, i] = squares.map((x) => pc_to_label(x));

        return `= [Next ${moves} moves / ${currentTurn} turn]
. +---+---+---+
. | ${a} | ${b} | ${c} |
. +---+---+---+
. | ${d} | ${e} | ${f} |
. +---+---+---+
. | ${g} | ${h} | ${i} |
. +---+---+---+
. moves ${this._record.toMovesString()}
.
`;
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
${indent}${this._turn.dump(indent + "    ")}`;
    }
}
