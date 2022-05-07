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

    setup(onSetMessageFromServer) {
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
            onSetMessageFromServer,
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