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
        console.log(`[setMessage] event=${event} text=${text} sq=${sq} myPiece=${myPiece}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "StoC_Start":
                // 対局開始の一斉通知
                vue1.init();   // 画面を初期化
                break;

            case "StoC_End":
                // 対局終了の一斉通知
                vue1.setState("EndOfGame"); // 画面を対局終了状態へ
                alert(text);                // 勝ち、または引分けの表示
                // vue1.init();   // 画面を初期化
                break;

            case "StoC_Move":
                // 指し手の一斉通知
                if (myPiece != vue1.engine.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    vue1.engine.game.makeMove(parseInt(sq), myPiece);
                    // 自分の手番に変更
                    vue1.engine.game.isMyTurn = true;
                    // 自分の手番ならアラートを常時表示
                    vue1.refreshVisibilityOfAlertYourMove();
                }
                break;

            default:
                console.log("No event");
        }
    };
}