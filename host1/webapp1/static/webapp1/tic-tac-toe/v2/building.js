/**
 * 建物
 */
class Building {
    /**
     * 生成
     * @param {*} setMessageFromServer - サーバーからのメッセージをセットする関数
     * @param {*} reconnect - 再接続ラムダ関数
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - 接続文字列を返す関数 (roomName, myPiece)=>{return connectionString;}
     * @param {function} setLabelOfButton - 升ボタンのラベルの設定
     */
    constructor(setMessageFromServer, reconnect, roomName, myPiece, convertPartsToConnectionString, setLabelOfButton) {
        this._setMessageFromServer = setMessageFromServer;
        this._reconnect = reconnect;

        // 接続
        this._connection = new Connection(roomName, myPiece, convertPartsToConnectionString(roomName, myPiece));

        // メッセージ一覧
        this._messageSender = new MessageSender();

        // 自分の駒
        this._myPiece = myPiece;

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

        // 局面
        this._position = new Position(this._myPiece);

        // ゲームオーバー集合
        this._gameoverSet = new GameoverSet();

        // ユーザーコントロール
        this._userCtrl = new UserCtrl();

        // 審判コントロール
        this._judgeCtrl = new JudgeCtrl();

        // 判断したとき
        this._judgeCtrl.onJudged = (pieceMoved, gameoverSetValue) => {
            this.gameoverSet.value = gameoverSetValue;
            let response;

            switch (gameoverSetValue) {
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
                    throw new Error(`Unexpected gameoverSetValue=${gameoverSetValue}`);
            }
        };

        this._setLabelOfButton = setLabelOfButton;

        // １手進めたとき
        this._userCtrl.onDoMove = (sq, pieceMoved) => {
            // ボタンのラベルを更新
            this._setLabelOfButton(sq, pieceMoved);

            console.log(`[Building onDoMove] this._myPiece=${this._myPiece} pieceMoved=${pieceMoved}`);

            // 自分の指し手なら送信
            if (this._myPiece == pieceMoved) {
                let response = this.messageSender.createDoMove(sq, pieceMoved);
                this._connection.webSock1.send(JSON.stringify(response));
            }
        };

        this.connect();
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
     * 局面
     */
    get position() {
        return this._position;
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
     * ゲームオーバー集合
     */
    get gameoverSet() {
        return this._gameoverSet;
    }

    /**
     * ボタンにラベルをセットする関数
     */
    get setLabelOfButton() {
        return this._setLabelOfButton;
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
     * 対局開始時
     */
    start() {
        console.log(`[Building start] myPiece=${this._connection.myPiece}`);

        // 勝者のクリアー
        this._winner = "";

        // ゲームオーバー状態のクリアー
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // 局面の初期化
        this._position = new Position(this._connection.myPiece);
        vue1.raisePositionChanged();
    }

    dump(indent) {
        return `
${indent}Building
${indent}--------
${indent}_myPiece:${this._myPiece}
${indent}_winner:${this._winner}
${indent}${this._gameoverSet.dump(indent + "    ")}
${indent}${this._position.dump(indent + "    ")}`;
    }
}
