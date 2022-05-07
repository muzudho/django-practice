// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

class Connection {
    constructor()
    {
        console.log(`[Debug] constructor`)
        this.roomName = document.forms["form1"]["room_name"].value;
        this.myPiece = document.forms["form1"]["my_piece"].value;
        this.connectionString = `ws://${window.location.host}/tic-tac-toe2/${this.roomName}/`;
        //                                                               ^
        //                      ---------------------------- -------------------------
        //                      1                            2
        // 1. ホスト アドレス
        // 2. URLの一部
    }

    /**
     * 
     * @param {*} onOpenWebSocket - on websocket open, send the START event.
     * @param {*} onCloseWebSocket - 例: サーバー側にエラーがあって接続が切れたりなど
     * @param {*} setMessage 
     */
    setup(onOpenWebSocket, onCloseWebSocket, setMessage) {
        console.log(`[Debug] Connection#setup`)
        this.webSock1 = new WebSocket(this.connectionString);

        this.webSock1.onopen = onOpenWebSocket;

        this.webSock1.onclose = onCloseWebSocket;

        // Sending the info about the room
        this.webSock1.onmessage = (e) => {
            // On getting the message from the server
            // Do the appropriate steps on each event.
            let data1 = JSON.parse(e.data);
            let message = data1["payload"];
            setMessage(message)
        };

        //call the connect function at the start.
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



