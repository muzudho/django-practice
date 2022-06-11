/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class MessageSenderV3 {
    /**
     * プレイヤーが部屋に入ります
     * @param {*} myPiece - X か O
     * @param {*} userId - ユーザーId
     * @returns メッセージ
     */
    checkin(myPiece, userId) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_Checkin",
            c2s_myPiece: myPiece,
            c2s_userId: userId,
        };
    }

    /**
     * プレイヤーが部屋から出ます
     * @param {*} myPiece - X か O
     * @param {*} userId - ユーザーId
     * @returns メッセージ
     */
    checkout(myPiece, userId) {
        // `c2s_` は クライアントからサーバーへ送る変数の目印
        return {
            c2s_event: "C2S_Checkout",
            c2s_myPiece: myPiece,
            c2s_userId: userId,
        };
    }
}
