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

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

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

        // 判断したとき
        this._judgeCtrl.onJudged = (pieceMoved, gameoverSet) => {
            this._playeq.gameoverState.value = gameoverSet;
            let response;

            switch (gameoverSet) {
                case GameoverSet.win:
                    // 勝ったとき
                    response = this.messageSender.createWon(pieceMoved);
                    this._connection.webSock1.send(JSON.stringify(response));
                    break;
                case GameoverSet.draw:
                    // 引き分けたとき
                    response = this.messageSender.createDraw();
                    this._connection.webSock1.send(JSON.stringify(response));
                    break;
                case GameoverSet.lose:
                    // 負けたとき
                    break;
                case GameoverSet.none:
                    // なんでもなかったとき
                    break;
                default:
                    throw new Error(`Unexpected gameoverSet=${gameoverSet}`);
            }
        };

        this.connect();
    }

    setup(setLabelOfButton) {
        // １手進めたとき
        this._userCtrl.onDoMove = (sq, pieceMoved) => {
            // ボタンのラベルを更新
            setLabelOfButton(sq, pieceMoved);

            console.log(`[onDoMove] this._myPiece=${this._myPiece} pieceMoved=${pieceMoved}`);

            // 自分の指し手なら送信
            if (this._myPiece == pieceMoved) {
                let response = this.messageSender.createDoMove(sq, pieceMoved);
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
     * 勝者
     */
    get winner() {
        return this._winner;
    }

    set winner(value) {
        this._winner = value;
    }

    /**
     * 対局結果
     */
    getGameoverSet() {
        // 勝者 "X", "O" を、勝敗 WIN, DRAW, LOSE, NONE に変換

        if (this._winner == PC_EMPTY_LABEL) {
            return GameoverSet.draw;
        } else if (this._winner == vue1.engine.connection.myPiece) {
            return GameoverSet.win;
        } else if (this._winner == flipTurn(vue1.engine.connection.myPiece)) {
            return GameoverSet.lose;
        }

        return GameoverSet.none;
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

    /**
     * 開始時
     */
    onStart() {
        console.log(`[Engine onStart] myPiece=${this._connection.myPiece}`);
        this._winner = "";

        this._playeq.onStart(this._connection.myPiece);
    }
}
