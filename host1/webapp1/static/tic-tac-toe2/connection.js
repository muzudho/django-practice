// 参考にした記事
// -------------
// 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

/**
 * 接続
 */
class Connection {

    constructor()
    {
        // 部屋名
        this.roomName = document.forms["form1"]["room_name"].value;

        // X か O か
        this.myPiece = document.forms["form1"]["my_piece"].value;

        // 接続文字列
        this.connectionString = `ws://${window.location.host}/tic-tac-toe2/${this.roomName}/`;
        //                                                               ^
        //                      ---------------------------- -------------------------------
        //                      1                            2
        // 1. ホスト アドレス
        // 2. URLの一部
        console.log(`[Debug] Connection#constructor roomName=${this.roomName} myPiece=${this.myPiece} connectionString=${this.connectionString}`)
    }

    /**
     * 設定
     * 
     * @param {*} onOpenWebSocket - Webソケットを開かれたとき
     * @param {*} onCloseWebSocket - Webソケットが閉じられたとき。 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {*} setMessageFromServer - サーバーからのメッセージがセットされる関数
     */
    setup(onOpenWebSocket, onCloseWebSocket, setMessageFromServer) {
        console.log(`[Debug] Connection#setup`)
        this.webSock1 = new WebSocket(this.connectionString);
        this.webSock1.onopen = onOpenWebSocket;
        this.webSock1.onclose = onCloseWebSocket;

        // 設定: サーバーからメッセージを受信したとき
        this.webSock1.onmessage = (e) => {
            // JSON を解析、メッセージだけ抽出
            let data1 = JSON.parse(e.data);
            let message = data1["message"];
            setMessageFromServer(message)
        };

        // Webソケットを接続します
        this.connect();
    }

    /**
     * Main function which handles the connection
     * of websocket.
     */
    connect() {
        if (this.webSock1.readyState == WebSocket.OPEN) {
            console.log('Open socket.');
            this.webSock1.onopen();
        }
    }
}
