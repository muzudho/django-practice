/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class MessageSender {
    /**
     * どちらかのプレイヤーが駒を置いたとき
     * @param {int} sq - 升番号
     * @param {string} pieceMoved - 駒を置いたプレイヤー。 X か O
     * @returns メッセージ
     */
    createDoMove(sq, pieceMoved) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        console.log(`[MessageSender createDoMove] sq=${sq} pieceMoved=${pieceMoved}`);
        return {
            c2s_event: "C2S_Moved",
            c2s_sq: sq,
            c2s_pieceMoved: pieceMoved,
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
     * @param {*} pieceMoved - 駒を置いた方の X か O
     * @returns メッセージ
     */
    createWon(pieceMoved) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_End",
            c2s_winner: pieceMoved,
        };
    }
}
