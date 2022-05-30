// 参考にした記事
// -------------
// 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

/**
 * 接続
 */
class Connection {
    constructor() {
        // 部屋名
        this._roomName = "";

        // X か O か
        this._myPiece = "";

        // 接続文字列（初期値はダミー文字列）
        this._connectionString = `ws://example.com/this/is/a/path/room_name/`;

        // 再接続中表示フラグ
        this.isReconnectingDisplay = false;
    }

    /**
     * セットアップ
     *
     * @param {string} roomName - 部屋名
     * @param {string} myPiece - X か O
     * @param {function} convertPartsToConnectionString - (roomName, myPiece) return connectionString
     */
    setup(roomName, myPiece, convertPartsToConnectionString) {
        this._roomName = roomName;
        this._myPiece = myPiece;
        this._connectionString = convertPartsToConnectionString(this._roomName, this._myPiece);
    }

    /**
     * 設定
     *
     * @param {*} onOpenWebSocket - Webソケットを開かれたとき
     * @param {*} onCloseWebSocket - Webソケットが閉じられたとき。 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {*} setMessageFromServer - サーバーからのメッセージがセットされる関数
     */
    connect(onOpenWebSocket, onCloseWebSocket, setMessageFromServer, onWebSocketError) {
        console.log(`[Connection#connect] Start`);

        // Webソケットを生成すると、接続も行われる。再接続したいときは、再生成する
        try {
            // 接続できないと、この生成に失敗する。catch もできない
            this.webSock1 = new WebSocket(this._connectionString);

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

            // 状態を表示
            if (this.webSock1.readyState == WebSocket.CONNECTING) {
                // 未接続
                console.log("[Connect] Connecting socket.");
            } else if (this.webSock1.readyState == WebSocket.OPEN) {
                console.log("[Connect] Open socket.");
                this.webSock1.onopen();
            } else if (this.webSock1.readyState == WebSocket.CLOSING) {
                console.log("[Connect] Closing socket.");
            } else if (this.webSock1.readyState == WebSocket.CLOSED) {
                // サーバーが落ちたりしたときは、ここ
                console.log("[Connect] Closed socket.");
            } else {
                console.log(`[Connect] webSock1.readyState=${this.webSock1.readyState}`);
            }
        } catch (error) {
            // キャッチで捕まえられない
            console.log(`[Connect] Exception ${error}`);
        }
    }
}
