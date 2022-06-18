/**
 * 受信メッセージ一覧
 */
class IncomingMessages {
    /**
     * サーバーからクライアントへ送られてきたメッセージをセットする関数を返します
     * @returns 関数
     */
    setMessageFromServer(message) {
        // `s2c_` は サーバーからクライアントへ送られてきた変数の目印
        // イベント
        let event = message["s2c_event"];
        console.log(`[IncomingMessages setMessageFromServer] サーバーからのメッセージを受信しました event:${event}`);

        switch (event) {
            case "S2C_Start":
                this.start(message);
                break;

            case "S2C_End":
                this.end(message);
                break;

            case "S2C_Moved":
                this.moved(message);
                break;

            default:
                // Undefined behavior
                console.log(`[IncomingMessages setMessageFromServer] ignored. event=[${event}]`);
        }
    }

    set onStart(value) {
        this._onStart = value;
    }

    set onEnd(value) {
        this._onEnd = value;
    }

    set onMoved(value) {
        this._onMoved = value;
    }

    /**
     * 対局開始時
     *
     * @param {*} message
     */
    start(message) {
        if (this._onStart == null) {
            // undefined も null も弾きます
            return;
        }

        console.log(`[IncomingMessages start]`);
        this._onStart(message);
    }

    /**
     * 対局終了時
     *
     * @param {*} message
     */
    end(message) {
        if (this._onEnd == null) {
            return;
        }

        // 勝者
        let winner = message["s2c_winner"];
        console.log(`[IncomingMessages end] winner:${winner}`);
        this._onEnd(message, winner);
    }

    /**
     * 指し手受信時
     *
     * @param {*} message
     */
    moved(message) {
        if (this._onMoved == null) {
            return;
        }

        // 升番号
        let sq = message["s2c_sq"];
        // 手番。 "X" か "O"
        let piece_moved = message["s2c_pieceMoved"];
        console.log(`[IncomingMessages onMoved] sq:${sq} piece_moved:${piece_moved}`);

        this._onMoved(message, parseInt(sq), piece_moved);
    }
}
