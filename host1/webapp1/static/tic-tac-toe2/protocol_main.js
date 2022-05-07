function createSetMessageFromServer() {
    return (message) => {
        let event = message["event"];
        let text = message["text"];
        let sq = message["sq"];
        let myPiece = message["myPiece"];
        console.log(`[setMessage] event=${event} text=${text} sq=${sq} myPiece=${myPiece}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "StoC_Start":
                vue1.reset();
                break;

            case "StoC_End":
                alert(text); // 勝ち、または引分けの表示
                vue1.reset();
                break;

            case "StoC_Move":
                if (myPiece != engine1.connection.myPiece) {
                    // 相手の手番なら、自動で動かします
                    engine1.game.makeMove(parseInt(sq), myPiece);
                    engine1.game.myTurn = true;
                    document.getElementById("alert_your_move").style.display = "block";
                }
                break;

            default:
                console.log("No event");
        }
    };
}