// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

const PC_EMPTY = -1 // A square without piece; PC is piece
const BOARD_AREA = 9 // All squares count

// Game board for maintaing the state of the game
let board = [
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

let connection;

// VueJSでの、ページ読込完了時
function onVueLoaded() {
    console.log(`[Debug] onVueLoaded`)

    var funcSetRequest = (event, message) => {
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
                if(message["player"] != myPiece){
                    makeMove(message["index"], message["player"])
                    myTurn = true;
                    document.getElementById("alert_move").style.display = 'block';
                }
                break;
            default:
                console.log("No event")
        }
    }

    connection = new Connection()
    connection.setup(funcSetRequest)
}

/**
 * 升ボタンをクリックしたとき
 * @param {*} sq - Square; 0 <= sq
 */
function clickSquare(sq) {
    console.log(`[Debug] clickSquare sq=${sq}`)
    if (board[sq] == PC_EMPTY) {
        if (!myTurn) {
            alert("Wait for other to place the move")
        }
        else {
            myTurn = false;
            document.getElementById("alert_move").style.display = 'none'; // Hide
            makeMove(sq, myPiece);
        }
    }
}

/**
 * Make a move
 * @param {*} sq - Square; 0 <= sq
 * @param {*} myPiece 
 * @returns 
 */
function makeMove(sq, myPiece){
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
                alert(`Invalid my piece = ${myPiece}`);
                return false;
        }

        webSock1.send(JSON.stringify(data))
    }
    // place the move in the game box.
    vue1.setPieceV(sq, myPiece);
    // check for the winner
    const gameOver = isGameOver();
    if(myTurn){
        // if player winner, send the END event.
        if(gameOver){
            data = {
                "event": "END",
                "message": `${myPiece} is a winner. Play again?`
            }
            webSock1.send(JSON.stringify(data))
        }
        else if(!gameOver && countOfMove == 9){
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
    console.log('[Debug] reset()');
    board = [
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
    ];
    countOfMove = 0;
    myTurn = true;
    document.getElementById("alert_move").style.display = 'block';

    // ボタンのラベルをクリアー
    for (let sq = 0; sq < BOARD_AREA; sq += 1){
        vue1.setPieceV(sq, "");
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
function isGameOver(){
    if (5 <= countOfMove) {
        for (let squaresOfWinPattern of arrayOfSquaresOfWinPattern) {
            if (isPieceInLine(squaresOfWinPattern)) {
                return true;
            }
        }
    }
    return false;
}
