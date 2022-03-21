// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

var roomName = document.getElementById("game_board").getAttribute("room_code");
var myPiece = document.getElementById("game_board").getAttribute("char_choice");

var connectionString = `ws://${window.location.host}/tic-tac-toe1/${roomName}/`;
//                           ----------------------- -------------------------
//                           1                       2
// 1. ホスト アドレス
// 2. URLの一部

var webSock1 = new WebSocket(connectionString);
// Game board for maintaing the state of the game
var board = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
];
// Winning indexes.
winSquares = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
let countOfMove = 0; // Number of moves done
let myTurn = true; // Boolean variable to get the turn of the player.

// Add the click event listener on every block.
let elementArrayOfSquare = document.getElementsByClassName('square');
for (var i = 0; i < elementArrayOfSquare.length; i++){
    elementArrayOfSquare[i].addEventListener("click", event=>{
        const sq = event.path[0].getAttribute('data-index'); // Square; 0 <= sq
        if(board[sq] == -1){
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

    if(board[sq] == -1){
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
    const win = checkWinner();
    if(myTurn){
        // if player winner, send the END event.
        if(win){
            data = {
                "event": "END",
                "message": `${myPiece} is a winner. Play again?`
            }
            webSock1.send(JSON.stringify(data))
        }
        else if(!win && countOfMove == 9){
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
        -1, -1, -1,
        -1, -1, -1,
        -1, -1, -1,
    ];
    countOfMove = 0;
    myTurn = true;
    document.getElementById("alert_move").style.display = 'inline';
    for (var i = 0; i < elementArrayOfSquare.length; i++){
        elementArrayOfSquare[i].innerHTML = "";
    }
}

/**
 * check if their is winning move
 * @param {*} patternOfWin 
 * @returns 
 */
const check = (patternOfWin) => {
    if (
      board[patternOfWin[0]] !== -1 &&
      board[patternOfWin[0]] === board[patternOfWin[1]] &&
      board[patternOfWin[0]] === board[patternOfWin[2]]
    )   return true;
    return false;
};

/**
 * function to check if player is winner.
 * @returns I won
 */
function checkWinner(){
    let win = false;
    if (5 <= countOfMove) {
      winSquares.forEach((w) => {
        if (check(w)) {
          win = true;
          windex = w;
        }
      });
    }
    return win;
}

// Main function which handles the connection
// of websocket.
function connect() {
    webSock1.onopen = function open() {
        console.log('WebSockets connection created.');
        // on websocket open, send the START event.
        webSock1.send(JSON.stringify({
            "event": "START",
            "message": ""
        }));
    };

    webSock1.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    // Sending the info about the room
    webSock1.onmessage = function (e) {
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
