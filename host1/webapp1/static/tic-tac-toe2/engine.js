class Engine {
    constructor() {
        this._connection = new Connection();
        this._protocol = new Protocol();
        this._game = new Game();
    }

    get connection() {
        return this._connection
    }

    get protocol() {
        return this._protocol
    }

    get game() {
        return this._game
    }

    setup() {
        this.connection.setup(
            // onOpenWebSocket
            () => {
                console.log('WebSockets connection created.');
                let response = this.protocol.createStart()
                this.connection.webSock1.send(JSON.stringify(response))
            },
            // onCloseWebSocket
            () => {
                console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
                setTimeout(function () {
                    this.connection.connect();
                }, 1000);
            },
            // setRequest
            (event, message) => {
                console.log(`[setRequest] event=${event}`); // ちゃんと動いているようなら消す

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
            },
        )


        // １手進めたとき
        this.game.onDoMove = (sq, myPiece) => {
            let response = this.protocol.createDoMove(sq, myPiece)
            this.connection.webSock1.send(JSON.stringify(response))
        }

        // どちらかが勝ったとき
        this.game.onWon = (myPiece) => {
            let response = this.protocol.createWon(myPiece)
            this.connection.webSock1.send(JSON.stringify(response))
        }

        // 引き分けたとき
        this.game.onDraw = () => {
            let response = this.protocol.createDraw()
            this.connection.webSock1.send(JSON.stringify(response))
        }
    }
}