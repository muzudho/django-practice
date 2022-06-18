// 参考にした記事
// -------------
// 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

/**
 * 接続
 */
class Connection {
    /**
     * ウェブソケット
     */
    #webSock1;

    /**
     * 生成
     *
     * @param {string} roomName - 部屋名
     * @param {strint} connectionString - Webソケット接続文字列
     * @param {IncommingMessages} incommingMessages - 受信メッセージ一覧
     * @param {function} onOpenWebSocket - Webソケットを開かれたとき
     * @param {function} onCloseWebSocket - Webソケットが閉じられたとき。 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {function} onWebSocketError - Webソケットエラー時のメッセージ
     * @param {function} onRetryWaiting - 再接続のためのインターバルの定期的なメッセージ
     * @param {function} onGiveUp - 再接続を諦めたとき
     */
    constructor(roomName, connectionString, incommingMessages, onOpenWebSocket, onCloseWebSocket, onWebSocketError, onRetryWaiting, onGiveUp) {
        // console.log(`[Connection constructor] roomName=[${roomName}] connectionString=[${connectionString}]`);

        // 部屋名
        this._roomName = roomName;

        // 接続文字列
        this._connectionString = connectionString;

        // リトライ回数
        this._retryCount = 0;
        // リトライ上限
        this._retryMax = 10;

        // 再接続のために記憶しておきます
        this._onOpenWebSocket = onOpenWebSocket;
        this._onCloseWebSocket = onCloseWebSocket;
        this._incommingMessages = incommingMessages;
        this._onWebSocketError = onWebSocketError;
        this._onRetryWaiting = onRetryWaiting;
        this._onGiveUp = onGiveUp;
    }

    /**
     * メッセージ送信
     */
    send(response) {
        this.#webSock1.send(JSON.stringify(response));
    }

    /**
     * 接続
     */
    connect() {
        // console.log(`[Connection#connect] Start this._connectionString=[${this._connectionString}]`);

        // Webソケット
        //
        // * 生成と同時に接続が始まる。そこで例外が起こるとキャッチはできないし、なぜか後続の処理に続かず関数を抜けてしまう
        // * １回切りの使い捨て。再接続機能は無い
        // * 再接続したいときは、再生成する
        try {
            this.#webSock1 = new WebSocket(this._connectionString);
            // 以下、接続に成功

            // イベントハンドラを毎回設定し直してください
            this.#webSock1.onopen = this._onOpenWebSocket;
            this.#webSock1.onclose = this._onCloseWebSocket;

            // 設定: サーバーからメッセージを受信したとき
            this.#webSock1.onmessage = (e) => {
                // JSON を解析、メッセージだけ抽出
                let data1 = JSON.parse(e.data);
                let message = data1["message"];
                this._incommingMessages.setMessageFromServer(message);
            };

            this.#webSock1.addEventListener("open", (event1) => {
                console.log("[Connection connect] WebSockets connection created.");
                // 再接続カウンターをリセットします
                this._retryCount = 0;
            });
            this.#webSock1.addEventListener("error", (event1) => {
                this._onWebSocketError(event1);
            });

            // 状態を表示
            if (this.#webSock1.readyState == WebSocket.CONNECTING) {
                // 未接続
                console.log("[Connection connect] Connecting socket.");
            } else if (this.#webSock1.readyState == WebSocket.OPEN) {
                console.log("[Connection connect] Open socket.");
                this.#webSock1.onopen();
            } else if (this.#webSock1.readyState == WebSocket.CLOSING) {
                console.log("[Connection connect] Closing socket.");
            } else if (this.#webSock1.readyState == WebSocket.CLOSED) {
                // サーバーが落ちたりしたときは、ここ
                console.log("[Connection connect] Closed socket.");

                // 再接続のリトライを書くタイミングはここです
                this.reconnect();
            } else {
                console.log(`[Connection connect] #webSock1.readyState=${this.#webSock1.readyState}`);
            }
        } catch (exception) {
            // キャッチで捕まえられない
            console.log(`[Connection connect] exception:${exception}`);
        }
    }

    /**
     * 再接続
     */
    reconnect() {
        if (this._retryMax <= this._retryCount) {
            // 諦めます
            console.log(`[Connection reconnect] Give up`);
            this._onGiveUp();
            return;
        }

        console.log(`[Connection reconnect] Start...`);

        // 再接続のインターバルの開始を通知しますが、実際に接続するのは５秒後です
        // 最初は 0 回目なので、表示を考慮して +1 の下駄を履かせます
        this._onRetryWaiting(true, this._retryCount + 1, this._retryMax);

        setTimeout(() => {
            console.log(`[Connection reconnect] Try... to:${this._connectionString}`);

            // 事前にカウントを上げておきます
            this._retryCount += 1;
            // 再接続のインターバルの終了を通知しますが、実際には接続を開始します
            this._onRetryWaiting(false, this._retryCount, this._retryMax);
            // 接続
            this.connect();
            console.log(`[Connection reconnect] End. retried:${this._retryCount}/${this._retryMax}`);
        }, 5000);
    }
}
