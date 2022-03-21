// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

var roomName = document.getElementById("game_board").getAttribute("room_code");
var myPiece = document.getElementById("game_board").getAttribute("char_choice");

var connectionString = `ws://${window.location.host}/tic-tac-toe1/${roomName}/`;
//                           ----------------------- -------------------------
//                           1                       2
// 1. ホスト アドレス
// 2. URLの一部

var webSock1 = new WebSocket(connectionString);

const PC_EMPTY = -1 // A square without piece; PC is piece
// Game board for maintaing the state of the game
var board = [
    PC_EMPTY, PC_EMPTY, PC_EMPTY,
    PC_EMPTY, PC_EMPTY, PC_EMPTY,
    PC_EMPTY, PC_EMPTY, PC_EMPTY,
];

// SQ is square
// +---------+
// | 0  1  2 |
// | 3  4  5 |
// | 6  7  8 |
// +---------+
const SQ_0 = 0
const SQ_1 = 1
const SQ_2 = 2
const SQ_3 = 3
const SQ_4 = 4
const SQ_5 = 5
const SQ_6 = 6
const SQ_7 = 7
const SQ_8 = 8
// Winning indexes.
arrayOfSquaresOfWinPattern = [
    // +---------+
    // | *  *  * |
    // | .  .  . |
    // | .  .  . |
    // +---------+
    [SQ_0, SQ_1, SQ_2],
    // +---------+
    // | .  .  . |
    // | *  *  * |
    // | .  .  . |
    // +---------+
    [SQ_3, SQ_4, SQ_5],
    // +---------+
    // | .  .  . |
    // | .  .  . |
    // | *  *  * |
    // +---------+
    [SQ_6, SQ_7, SQ_8],
    // +---------+
    // | *  .  . |
    // | *  .  . |
    // | *  .  . |
    // +---------+
    [SQ_0, SQ_3, SQ_6],
    // +---------+
    // | .  *  . |
    // | .  *  . |
    // | .  *  . |
    // +---------+
    [SQ_1, SQ_4, SQ_7],
    // +---------+
    // | .  .  * |
    // | .  .  * |
    // | .  .  * |
    // +---------+
    [SQ_2, SQ_5, SQ_8],
    // +---------+
    // | *  .  . |
    // | .  *  . |
    // | .  .  * |
    // +---------+
    [SQ_0, SQ_4, SQ_8],
    // +---------+
    // | .  .  * |
    // | .  *  . |
    // | *  .  . |
    // +---------+
    [SQ_2, SQ_4, SQ_6]
]
let countOfMove = 0; // Number of moves done
let myTurn = true; // Boolean variable to get the turn of the player.

// Add the click event listener on every block.
let elementArrayOfSquare = document.getElementsByClassName('square');
for (var i = 0; i < elementArrayOfSquare.length; i++){
    elementArrayOfSquare[i].addEventListener("click", event=>{
        const sq = event.path[0].getAttribute('data-index'); // Square; 0 <= sq
        if(board[sq] == PC_EMPTY){
            if(!myTurn){
                alert("Wait for other to place the move")
            }
            else{
                myTurn = false;
                document.getElementById("alert_move").style.display = 'none'; // Hide
                make_move(sq, myPiece);
            }
        }
    })
}

/**
 * Make a move
 * @param {*} sq - Square; 0 <= sq
 * @param {*} myPiece 
 * @returns 
 */
function make_move(sq, myPiece){
    sq = parseInt(sq);
    let data = {
        "event": "MOVE",
        "message": {
            "index": sq,
            "player": myPiece
        }
    }

    if(board[sq] == PC_EMPTY){
        // if the valid move, update the board
        // state and send the move to the server.
        countOfMove++;

        switch (myPiece) {
            case 'X':
                board[sq] = 1;
                break;
            case 'O':
                board[sq] = 0;
                break;
            default:
                alert("Invalid character choice");
                return false;
        }

        webSock1.send(JSON.stringify(data))
    }
    // place the move in the game box.
    elementArrayOfSquare[sq].innerHTML = myPiece;
    // check for the winner
    const isGameOver = IsGameOver();
    if(myTurn){
        // if player winner, send the END event.
        if(isGameOver){
            data = {
                "event": "END",
                "message": `${myPiece} is a winner. Play again?`
            }
            webSock1.send(JSON.stringify(data))
        }
        else if(!isGameOver && countOfMove == 9){
            data = {
                "event": "END",
                "message": "It's a draw. Play again?"
            }
            webSock1.send(JSON.stringify(data))
        }
    }
}

// function to reset the game.
function reset(){
    board = [
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
    ];
    countOfMove = 0;
    myTurn = true;
    document.getElementById("alert_move").style.display = 'inline';
    for (const element of elementArrayOfSquare) {
        element.innerHTML = "";
    }
}

/**
 * check if their is winning move
 * @param {*} squaresOfWinPattern 
 * @returns 
 */
function isPieceInLine(squaresOfWinPattern) {
    return board[squaresOfWinPattern[0]] !== PC_EMPTY &&
        board[squaresOfWinPattern[0]] === board[squaresOfWinPattern[1]] &&
        board[squaresOfWinPattern[0]] === board[squaresOfWinPattern[2]];
}

/**
 * function to check if player is winner.
 * @returns I won
 */
function IsGameOver(){
    if (5 <= countOfMove) {
        for (let squaresOfWinPattern of arrayOfSquaresOfWinPattern) {
            if (isPieceInLine(squaresOfWinPattern)) {
                return true;
            }
        }
    }
    return false;
}

/**
 * Main function which handles the connection
 * of websocket.
 */
function connect() {
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
        let data = JSON.parse(e.data);
        data = data["payload"];
        let message = data['message'];
        let event = data["event"];
        switch (event) {
            case "START":
                console.log(`[Message] START e=${e.data}`); // ちゃんと動いているようなら消す
                reset();
                break;
            case "END":
                console.log(`[Message] END e=${e.data}`); // ちゃんと動いているようなら消す
                alert(message);
                reset();
                break;
            case "MOVE":
                console.log(`[Message] MOVE e=${e.data}`); // ちゃんと動いているようなら消す
                if(message["player"] != myPiece){
                    make_move(message["index"], message["player"])
                    myTurn = true;
                    document.getElementById("alert_move").style.display = 'inline';
                }
                break;
            default:
                console.log(`[Message] (Others) e=${e.data}`); // ちゃんと動いているようなら消す
                console.log("No event")
        }
    };

    if (webSock1.readyState == WebSocket.OPEN) {
        console.log('Open socket.');
        webSock1.onopen();
    }
}

//call the connect function at the start.
connect();
