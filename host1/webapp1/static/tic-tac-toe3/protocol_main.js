/**
 * サーバーからのメッセージをセットする関数を返します
 * @returns 関数
 */
function createSetMessageFromServer() {
    return (message) => {
        // イベント
        let event = message["event"];
        // テキスト
        let text = message["text"];
        // 升番号
        let sq = message["sq"];
        // X か O
        let myPiece = message["myPiece"];
        // 勝者
        let winner = message["winner"];
        console.log(`[setMessage] event=${event} text=${text} sq=${sq} myPiece=${myPiece} winner=${winner}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "StoC_Start":
                // 対局開始の一斉通知
                vue1.init();   // 画面を初期化
                break;

            case "StoC_End":
                // 対局終了の一斉通知
                let result;
                if (winner == PC_EMPTY_LABEL) {
                    result = RESULT_DRAW
                } else if (winner == vue1.engine.connection.myPiece) {
                    result = RESULT_WON
                } else {
                    result = RESULT_LOST
                }

                vue1.setGameIsOver(result);
                break;

            case "StoC_Move":
                // 指し手の一斉通知
                if (myPiece != vue1.engine.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    vue1.engine.game.makeMove(parseInt(sq), myPiece);
                    vue1.engine.judge.judge(myPiece);

                    // 自分の手番に変更
                    vue1.engine.game.isMyTurn = true;
                    vue1.engine.game.isWaitForOther = false;
                }
                break;

            default:
                console.log("No event");
        }
    };
}
