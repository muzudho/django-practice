// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
let connection;
let game;

// VueJSでの、ページ読込完了時
function onVueLoaded() {
    console.log(`[Debug] onVueLoaded`)

    game = new Game()

    connection = new Connection()

    connection.setup((event, message) => {
        console.log(`[setRequest] event=${event} message=${message}`); // ちゃんと動いているようなら消す
        switch (event) {
            case "START":
                reset();
                break;
            case "END":
                alert(message);
                reset();
                break;
            case "MOVE":
                if(message["player"] != connection.myPiece){
                    game.makeMove(parseInt(message["index"]), message["player"])
                    game.myTurn = true;
                    document.getElementById("alert_move").style.display = 'block';
                }
                break;
            default:
                console.log("No event")
        }
    })
}

/**
 * 升ボタンをクリックしたとき
 * @param {*} sq - Square; 0 <= sq
 */
function clickSquare(sq) {
    console.log(`[Debug] clickSquare sq=${sq}`)
    if (game.board[sq] == PC_EMPTY) {
        if (!game.myTurn) {
            alert("Wait for other to place the move")
        }
        else {
            game.myTurn = false;
            document.getElementById("alert_move").style.display = 'none'; // Hide
            game.makeMove(parseInt(sq), connection.myPiece);
        }
    }
}

// function to reset the game.
function reset() {
    console.log('[Debug] view_model#reset()');

    game.reset()

    document.getElementById("alert_move").style.display = 'block';

    // ボタンのラベルをクリアー
    for (let sq = 0; sq < BOARD_AREA; sq += 1){
        vue1.setPieceV(sq, "");
    }
}
