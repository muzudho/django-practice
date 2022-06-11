/**
 * ゲームエンジン
 */
class Engine {
    /**
     * 生成
     * @param {*} setMessageFromServer - サーバーからのメッセージをセットする関数
     * @param {*} reconnect - 再接続ラムダ関数
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
     */
    constructor(setMessageFromServer, reconnect, roomName, myPiece, convertPartsToConnectionString) {
        this._setMessageFromServer = setMessageFromServer;
        this._reconnect = reconnect;

        // 自分の駒
        this._myPiece = myPiece;

        // 接続
        this._connection = new Connection();
        this._connection.setup(roomName, myPiece, convertPartsToConnectionString);

        // メッセージ一覧
        this._messageSender = new MessageSender();

        // 遊具
        this._playeq = new PlaygroundEquipment();

        // ユーザーコントロール
        this._userCtrl = new UserCtrl(this._playeq);

        // 審判コントロール
        this._judgeCtrl = new JudgeCtrl(this._playeq, this._userCtrl);

        // どちらかが勝ったとき
        this._judgeCtrl.onWon = (myPiece) => {
            let response = this.messageSender.createWon(myPiece);
            this._connection.webSock1.send(JSON.stringify(response));
        };

        // 引き分けたとき
        this._judgeCtrl.onDraw = () => {
            let response = this.messageSender.createDraw();
            this._connection.webSock1.send(JSON.stringify(response));
        };

        this.connect();
    }

    setup(setLabelOfButton) {
        // １手進めたとき
        this._userCtrl.onDoMove = (sq, piece) => {
            // ボタンのラベルを更新
            setLabelOfButton(sq, piece);

            console.log(`[onDoMove] this._myPiece=${this._myPiece} piece=${piece}`);

            // 自分の指し手なら送信
            if (this._myPiece == piece) {
                let response = this.messageSender.createDoMove(sq, piece);
                this._connection.webSock1.send(JSON.stringify(response));
            }
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
    get messageSender() {
        return this._messageSender;
    }

    /**
     * 遊具
     */
    get playeq() {
        return this._playeq;
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
                let response = this.messageSender.createStart();
                this._connection.webSock1.send(JSON.stringify(response));
            },
            // Webソケットが閉じられたとき
            (e) => {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`);
                // 1回だけ再接続を試みます
                this._reconnect();
            },
            // サーバーからのメッセージを受信したとき
            this._setMessageFromServer,
            // エラー時
            (e) => {
                console.log(`Socket is error. ${e.reason}`);
            }
        );
    }
}
