let roomName;
let myPiece;
let connectionString;
let webSock1;

function connection_setup(setRequest) {
    console.log(`[Debug] connection_setup`)
    roomName = document.forms["form1"]["room_name"].value;
    myPiece = document.forms["form1"]["my_piece"].value;
    connectionString = `ws://${window.location.host}/tic-tac-toe2/${roomName}/`;
    //                                                          ^
    //                  ---------------------------- -------------------------
    //                  1                            2
    // 1. ホスト アドレス
    // 2. URLの一部

    webSock1 = new WebSocket(connectionString);

    // on websocket open, send the START event.
    webSock1.onopen = () => {
        console.log('WebSockets connection created.');
        webSock1.send(JSON.stringify({
            "event": "START",
            "message": ""
        }));
    };

    webSock1.onclose = (e) => {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    // Sending the info about the room
    webSock1.onmessage = (e) => {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data1 = JSON.parse(e.data);
        let data2 = data1["payload"];
        let message = data2['message'];
        let event = data2["event"];

        setRequest(event, message)

        switch (event) {
            case "START":
                reset();
                break;
            case "END":
                alert(message);
                reset();
                break;
            case "MOVE":
                if(message["player"] != myPiece){
                    makeMove(message["index"], message["player"])
                    myTurn = true;
                    document.getElementById("alert_move").style.display = 'block';
                }
                break;
            default:
                console.log("No event")
        }
    };

    //call the connect function at the start.
    connect();
}

/**
 * Main function which handles the connection
 * of websocket.
 */
function connect() {
    if (webSock1.readyState == WebSocket.OPEN) {
        console.log('Open socket.');
        webSock1.onopen();
    }
}
