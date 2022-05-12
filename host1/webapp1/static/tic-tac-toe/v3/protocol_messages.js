/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class ProtocolMessages {

    /**
     * どちらかのプレイヤーが石を置いたとき
     * @param {*} sq - 升番号
     * @param {*} myPiece - X か O
     * @returns メッセージ
     */
    createDoMove(sq, myPiece) {
        return {
            "event": "CtoS_Move",
            "sq": sq,
            "myPiece": myPiece,
        }
    }

    /**
     * 引き分けたとき
     * @returns メッセージ
     */
    createDraw() {
        return {
            "event": "CtoS_End",
            "winner": PC_EMPTY_LABEL,
        }
    }

    /**
     * 対局を開始したとき
     * @returns メッセージ
     */
    createStart() {
        return {
            "event": "CtoS_Start",
        }
    }

    /**
     * どちらかのプレイヤーが勝ったとき
     * @param {*} myPiece - X か O
     * @returns メッセージ
     */
    createWon(myPiece) {
        return {
            "event": "CtoS_End",
            "winner": myPiece,
        }
    }
}
