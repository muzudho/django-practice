/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class MessageSender {
    /**
     * どちらかのプレイヤーが石を置いたとき
     * @param {string} roomName - 部屋名
     * @param {int} sq - 升番号
     * @param {string} myPiece - X か O
     * @returns メッセージ
     */
    createDoMove(roomName, sq, myPiece) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_Move",
            c2s_roomName: roomName,
            c2s_sq: sq,
            c2s_myPiece: myPiece,
        };
    }

    /**
     * 引き分けたとき
     * @returns メッセージ
     */
    createDraw() {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_End",
            c2s_winner: PC_EMPTY_LABEL,
        };
    }

    /**
     * 対局を開始したとき
     * @returns メッセージ
     */
    createStart() {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_Start",
        };
    }

    /**
     * どちらかのプレイヤーが勝ったとき
     * @param {*} myPiece - X か O
     * @returns メッセージ
     */
    createWon(myPiece) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_End",
            c2s_winner: myPiece,
        };
    }
}
