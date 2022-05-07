class Protocol {
    constructor() {
    }

    setup() {
        engine1.connection.setup((event, message) => {
            console.log(`[engine1.connection.setup] event=${event}`); // ちゃんと動いているようなら消す

            switch (event) {
                case "E_Start":
                    vue1.reset();
                    break;

                case "E_End":
                    alert(`${message}`); // 勝ち、または引分けの表示
                    vue1.reset();
                    break;

                case "E_Move":
                    if(message["player"] != engine1.connection.myPiece){
                        engine1.game.makeMove(parseInt(message["index"]), message["player"])
                        engine1.game.myTurn = true;
                        document.getElementById("alert_your_move").style.display = 'block';
                    }
                    break;

                default:
                    console.log("No event")
            }
        })
    }

    /**
     * if player winner, send the END event.
     */
    sendWon(myPiece) {
        engine1.connection.webSock1.send(JSON.stringify(
            {
                "event": "E_End",
                "message": `${myPiece} is a winner. Play again?`
            }
        ))
    }

    sendDraw() {
        engine1.connection.webSock1.send(JSON.stringify(
            {
                "event": "E_End",
                "message": "It's a draw. Play again?"
            }
        ))
    }

    sendDoMove(sq, myPiece) {
        engine1.connection.webSock1.send(JSON.stringify(
            {
                "event": "E_Move",
                "message":
                {
                    "index": sq,
                    "player": myPiece
                }
            }
        ))
    }

    sendStart() {
        engine1.connection.webSock1.send(JSON.stringify({
            "event": "E_Start",
            "message": ""
        }));
    }
}
