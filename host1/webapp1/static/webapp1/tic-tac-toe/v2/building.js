/**
 * 建物
 */
class Building {
    /**
     * 生成
     * @param {string} myTurn - 自分の手番。 "X" か "O"。 部屋に入ると変えることができない
     * @param {function} setLabelOfButton - 升ボタンのラベルの設定
     */
    constructor(myTurn, setLabelOfButton) {
        console.log(`[Building constructor] 自分の手番=${myTurn}`);

        // メッセージ一覧
        this._messageSender = new MessageSender();

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

        // 局面
        this._position = new Position(myTurn);

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
                    vue1.connection.webSock1.send(JSON.stringify(response));
                    break;
                case GameoverSet.draw:
                    // 引き分けたとき
                    response = this.messageSender.createDraw();
                    vue1.connection.webSock1.send(JSON.stringify(response));
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

            console.log(`[Building onDoMove] 自分の手番=${this._position.turn.me} pieceMoved=${pieceMoved}`);

            // 自分の指し手なら送信
            if (this._position.turn.me == pieceMoved) {
                let response = this.messageSender.createDoMove(sq, pieceMoved);
                vue1.connection.webSock1.send(JSON.stringify(response));
            }
        };
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
     * 対局開始時
     */
    start() {
        console.log(`[Building start] 自分の手番=${this._position.turn.me}`);

        // 勝者のクリアー
        this._winner = "";

        // ゲームオーバー状態のクリアー
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // 局面の初期化
        this._position = new Position(this._position.turn.me);
        vue1.raisePositionChanged();
    }

    dump(indent) {
        return `
${indent}Building
${indent}--------
${indent}_winner:${this._winner}
${indent}${this._gameoverSet.dump(indent + "    ")}
${indent}${this._position.dump(indent + "    ")}`;
    }
}
