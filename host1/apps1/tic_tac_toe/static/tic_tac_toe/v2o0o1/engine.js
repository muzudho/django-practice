/**
 * 思考エンジン
 */
class Engine {
    /**
     * 生成
     * @param {string} myTurn - 自分の手番。 "X" か "O"。 部屋に入ると変えることができない
     * @param {UserCtrl} userCtrl - ユーザーコントロール
     * @param {JudgeCtrl} judgeCtrl - 審判コントロール
     */
    constructor(myTurn, userCtrl, judgeCtrl) {
        console.log(`[Engine constructor] 自分の手番=${myTurn}`);

        // あれば勝者 "X", "O" なければ空文字列
        this._winner = "";

        // 局面
        this._position = new Position(myTurn);

        // ゲームオーバー集合
        this._gameoverSet = new GameoverSet();

        // ユーザーコントロール
        this._userCtrl = userCtrl;

        // 審判コントロール
        this._judgeCtrl = judgeCtrl;
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
     * 対局開始時
     */
    start() {
        console.log(`[Engine start] 自分の手番=${this._position.turn.me}`);

        // 勝者のクリアー
        this._winner = "";

        // ゲームオーバー状態のクリアー
        this._gameoverSet = new GameoverSet(GameoverSet.none);

        // 局面の初期化
        this._position = new Position(this._position.turn.me);
    }

    /**
     * コマンドの実行
     */
    execute(command) {
        switch (command) {
            case "board":
                return this._position.toBoardString();
            default:
                // ignored
                return "";
        }
    }

    dump(indent) {
        return `
${indent}Engine
${indent}------
${indent}_winner:${this._winner}
${indent}${this._gameoverSet.dump(indent + "    ")}
${indent}${this._position.dump(indent + "    ")}`;
    }
}
