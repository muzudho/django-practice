let roomName;
let myPiece;
let connectionString;
let webSock1;

function connection_setup() {
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
}