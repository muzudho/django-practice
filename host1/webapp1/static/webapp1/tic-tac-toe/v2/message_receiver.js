/**
 * サーバーからクライアントへ送られてきたメッセージをセットする関数を返します
 * @returns 関数
 */
function packSetMessageFromServer() {
    return (message) => {
        // `s2c_` は サーバーからクライアントへ送られてきた変数の目印
        // イベント
        let event = message["s2c_event"];
        // 升番号
        let sq = message["s2c_sq"];
        // 手番。 "X" か "O"
        let piece_moved = message["s2c_pieceMoved"];
        // 勝者
        let winner = message["s2c_winner"];
        console.log(`[setMessage] サーバーからのメッセージを受信しました event=${event} sq=${sq} piece_moved=${piece_moved} winner=${winner}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "S2C_Start":
                // 対局開始時
                console.log(`[setMessage] S2C_Start`);
                vue1.onStart();
                break;

            case "S2C_End":
                // 対局終了時
                vue1.onGameover(winner);
                break;

            case "S2C_Moved":
                // 指し手受信時
                console.log(`[setMessage] S2C_Moved piece_moved=${piece_moved} myPiece=${vue1.engine.connection.myPiece}`);

                if (piece_moved != vue1.engine.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    vue1.engine.userCtrl.doMove(parseInt(sq), piece_moved);

                    // 自分の手番に変更
                    vue1.engine.playeq.myTurn.isTrue = true;

                    // クリアー
                    vue1.engine.playeq.isVisibleAlertWaitForOther = false;
                    // v-showが働かなかったので、シンプルな変数に写す
                    vue1.isVisibleAlertWaitForOtherFlag = vue1.engine.playeq.isVisibleAlertWaitForOther;
                }

                // どちらの手番でもゲームオーバー判定は行います
                vue1.engine.judgeCtrl.doJudge(piece_moved);

                break;

            default:
                // Undefined behavior
                console.log(`[setMessage] ignored. event=[${event}]`);
        }
    };
}
