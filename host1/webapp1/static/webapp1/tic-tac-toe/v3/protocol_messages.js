/**
 * メッセージ一覧
 *
 * * クライアントからサーバーへ送る
 */
class ProtocolMessagesV3 {
    /**
     * プレイヤーが部屋に入ります
     * @param {*} roomName - 部屋名
     * @param {*} myPiece - X か O
     * @param {*} userId - ユーザーId
     * @returns メッセージ
     */
    checkin(roomName, myPiece, userId) {
        return {
            event: "CtoS_Checkin",
            roomName: roomName,
            myPiece: myPiece,
            userId: userId,
        };
    }

    /**
     * プレイヤーが部屋から出ます
     * @param {*} roomName - 部屋名
     * @param {*} myPiece - X か O
     * @param {*} userId - ユーザーId
     * @returns メッセージ
     */
    checkout(roomName, myPiece, userId) {
        return {
            event: "CtoS_Checkout",
            roomName: roomName,
            myPiece: myPiece,
            userId: userId,
        };
    }
}
