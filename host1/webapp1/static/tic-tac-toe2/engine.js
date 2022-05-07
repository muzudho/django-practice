/**
 * ゲームエンジン
 */
class Engine {
    constructor() {
        // 接続
        this._connection = new Connection();
        // メッセージ一覧
        this._protocolMessages = new ProtocolMessages();
        // ゲーム
        this._game = new Game();
    }

    /**
     * 接続
     */
    get connection() {
        return this._connection
    }

    /**
     * メッセージ一覧
     */
    get protocolMessages() {
        return this._protocolMessages
    }

    /**
     * ゲーム
     */
    get game() {
        return this._game
    }

    /**
     * 準備
     * @param {*} onSetMessageFromServer - サーバーからのメッセージをセットする関数
     */
    setup(onSetMessageFromServer) {
        this.connection.setup(
            // Webソケットを開かれたとき
            () => {
                console.log('WebSockets connection created.');
                let response = this.protocolMessages.createStart()
                this.connection.webSock1.send(JSON.stringify(response))
            },
            // Webソケットが閉じられたとき
            () => {
                console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
                setTimeout(function () {
                    this.connection.connect();
                }, 1000);
            },
            // サーバーからのメッセージを受信したとき
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