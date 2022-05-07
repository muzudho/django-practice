class Engine {
    constructor() {
        this._connection = new Connection();
        this._protocolMessages = new ProtocolMessages();
        this._game = new Game();
    }

    get connection() {
        return this._connection
    }

    get protocolMessages() {
        return this._protocolMessages
    }

    get game() {
        return this._game
    }

    setup() {
        this.connection.setup(
            // onOpenWebSocket
            () => {
                console.log('WebSockets connection created.');
                let response = this.protocolMessages.createStart()
                this.connection.webSock1.send(JSON.stringify(response))
            },
            // onCloseWebSocket
            () => {
                console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
                setTimeout(function () {
                    this.connection.connect();
                }, 1000);
            },
            // setMessage
            (message) => {
                let event = message["event"];
                let text = message['text'];
                let sq = message['sq'];
                let myPiece = message['myPiece'];
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
                            engine1.game.makeMove(parseInt(sq), myPiece)
                            engine1.game.myTurn = true;
                            document.getElementById("alert_your_move").style.display = 'block';
                        }
                        break;

                    default:
                        console.log("No event")
                }
            },
        )


        // １手進めたとき
        this.game.onDoMove = (sq, myPiece) => {
            let response = this.protocolMessages.createDoMove(sq, myPiece)
            this.connection.webSock1.send(JSON.stringify(response))
        }

        // どちらかが勝ったとき
        this.game.onWon = (myPiece) => {
            let response = this.protocolMessages.createWon(myPiece)
            this.connection.webSock1.send(JSON.stringify(response))
        }

        // 引き分けたとき
        this.game.onDraw = () => {
            let response = this.protocolMessages.createDraw()
            this.connection.webSock1.send(JSON.stringify(response))
        }
    }
}