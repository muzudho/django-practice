// 参考にした記事
// -------------
// 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

/**
 * 接続
 */
class Connection {
    /**
     * 生成
     *
     * @param {string} roomName - 部屋名
     * @param {strint} connectionString - Webソケット接続文字列
     * @param {*} onOpenWebSocket - Webソケットを開かれたとき
     * @param {*} onCloseWebSocket - Webソケットが閉じられたとき。 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {*} setMessageFromServer - サーバーからのメッセージがセットされる関数
     * @param {*} onWebSocketError - Webソケットエラー時のメッセージ
     */
    constructor(roomName, connectionString, onOpenWebSocket, onCloseWebSocket, setMessageFromServer, onWebSocketError) {
        // console.log(`[Connection constructor] roomName=[${roomName}] connectionString=[${connectionString}]`);

        // 部屋名
        this._roomName = roomName;

        // 接続文字列
        this._connectionString = connectionString;

        // 再接続中表示フラグ
        this.isReconnectingDisplay = false;

        try {
            // 接続できないと、この生成に失敗する。catch もできない
            this.webSock1 = new WebSocket(this._connectionString);
            // console.log(`[Debug][Connection#connect] Connecting...`);

            this.webSock1.onopen = onOpenWebSocket;
            this.webSock1.onclose = onCloseWebSocket;

            // 設定: サーバーからメッセージを受信したとき
            this.webSock1.onmessage = (e) => {
                // JSON を解析、メッセージだけ抽出
                let data1 = JSON.parse(e.data);
                let message = data1["message"];
                setMessageFromServer(message);
            };

            // this.webSock1.onerror = onWebSocketError;
            this.webSock1.addEventListener("error", (event1) => {
                onWebSocketError(event1);
            });
        } catch (exception) {
            // キャッチで捕まえられない
            console.log(`[Connection constructor] exception:${exception}`);
        }
    }

    /**
     * 接続
     */
    connect() {
        // console.log(`[Connection#connect] Start this._connectionString=[${this._connectionString}]`);

        // Webソケットを生成すると、接続も行われる。再接続したいときは、再生成する
        try {
            // 状態を表示
            if (this.webSock1.readyState == WebSocket.CONNECTING) {
                // 未接続
                console.log("[Connection connect] Connecting socket.");
            } else if (this.webSock1.readyState == WebSocket.OPEN) {
                console.log("[Connection connect] Open socket.");
                this.webSock1.onopen();
            } else if (this.webSock1.readyState == WebSocket.CLOSING) {
                console.log("[Connection connect] Closing socket.");
            } else if (this.webSock1.readyState == WebSocket.CLOSED) {
                // サーバーが落ちたりしたときは、ここ
                console.log("[Connection connect] Closed socket.");
            } else {
                console.log(`[Connection connect] webSock1.readyState=${this.webSock1.readyState}`);
            }
        } catch (exception) {
            // キャッチで捕まえられない
            console.log(`[Connection connect] exception:${exception}`);
        }
    }
}
