/**
 * ゲームエンジン
 */
class Engine {
    /**
     * 生成
     * @param {*} onSetMessageFromServer - サーバーからのメッセージをセットする関数
     * @param {*} reconnect - 再接続ラムダ関数
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
     */
    constructor(onSetMessageFromServer, reconnect, roomName, myPiece, convertPartsToConnectionString) {
        this._onSetMessageFromServer = onSetMessageFromServer;
        this._reconnect = reconnect;

        // 接続
        this._connection = new Connection();

        this._connection.setup(roomName, myPiece, convertPartsToConnectionString);

        // メッセージ一覧
        this._protocolMessages = new ProtocolMessages();
        // ユーザーコントロール
        this._userCtrl = new UserCtrl();
        // 審判コントロール
        this._judgeCtrl = new JudgeCtrl(this._userCtrl);

        // どちらかが勝ったとき
        this._judgeCtrl.onWon = (myPiece) => {
            let response = this.protocolMessages.createWon(myPiece);
            this._connection.webSock1.send(JSON.stringify(response));
        };

        // 引き分けたとき
        this._judgeCtrl.onDraw = () => {
            let response = this.protocolMessages.createDraw();
            this._connection.webSock1.send(JSON.stringify(response));
        };

        this.connect();
    }

    setup(setLabelOfButton) {
        // １手進めたとき
        this._userCtrl.onDoMove = (sq, myPiece) => {
            // ボタンのラベルを更新
            setLabelOfButton(sq, myPiece);

            let response = this.protocolMessages.createDoMove(sq, myPiece);
            this._connection.webSock1.send(JSON.stringify(response));
        };
    }

    /**
     * 接続
     */
    get connection() {
        return this._connection;
    }

    /**
     * メッセージ一覧
     */
    get protocolMessages() {
        return this._protocolMessages;
    }

    /**
     * ユーザーコントロール
     */
    get userCtrl() {
        return this._userCtrl;
    }

    /**
     * 審判コントロール
     */
    get judgeCtrl() {
        return this._judgeCtrl;
    }

    /**
     * 接続
     */
    connect() {
        this._connection.connect(
            // Webソケットを開かれたとき
            () => {
                console.log("WebSockets connection created.");
                let response = this.protocolMessages.createStart();
                this._connection.webSock1.send(JSON.stringify(response));
            },
            // Webソケットが閉じられたとき
            (e) => {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`);
                // 1回だけ再接続を試みます
                this._reconnect();
            },
            // サーバーからのメッセージを受信したとき
            this._onSetMessageFromServer,
            // エラー時
            (e) => {
                console.log(`Socket is error. ${e.reason}`);
            }
        );
    }
}
