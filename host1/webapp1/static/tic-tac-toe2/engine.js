/**
 * ゲームエンジン
 */
class Engine {
    /**
     * 生成
     * @param {*} onSetMessageFromServer - サーバーからのメッセージをセットする関数
     * @param {*} reconnect - 再接続ラムダ関数
     */
    constructor(onSetMessageFromServer, reconnect) {
        this._onSetMessageFromServer = onSetMessageFromServer
        this._reconnect = reconnect

        // 接続
        this._connection = new Connection();
        // メッセージ一覧
        this._protocolMessages = new ProtocolMessages();
        // ゲーム
        this._game = new Game();

        // １手進めたとき
        this._game.onDoMove = (sq, myPiece) => {
            let response = this.protocolMessages.createDoMove(sq, myPiece)
            this._connection.webSock1.send(JSON.stringify(response))
        }

        // どちらかが勝ったとき
        this._game.onWon = (myPiece) => {
            let response = this.protocolMessages.createWon(myPiece)
            this._connection.webSock1.send(JSON.stringify(response))
        }

        // 引き分けたとき
        this._game.onDraw = () => {
            let response = this.protocolMessages.createDraw()
            this._connection.webSock1.send(JSON.stringify(response))
        }

        this.connect()
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
     * 接続
     */
    connect() {
        this._connection.connect(
            // Webソケットを開かれたとき
            () => {
                console.log('WebSockets connection created.');
                let response = this.protocolMessages.createStart()
                this._connection.webSock1.send(JSON.stringify(response))
            },
            // Webソケットが閉じられたとき
            (e) => {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`);
                // 1回だけ再接続を試みます
                this._reconnect()
            },
            // サーバーからのメッセージを受信したとき
            this._onSetMessageFromServer,
            // エラー時
            (e) => {
                console.log(`Socket is error. ${e.reason}`);
            }
        )
    }
}
