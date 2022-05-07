
const PC_EMPTY = -1 // A square without piece; PC is piece
const BOARD_AREA = 9 // All squares count

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
WIN_PATTERN = [
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

class Game {
    constructor() {
        console.log('[Debug] Game#constructor()');
        this.reset()

        this._doMove = () => {
            // Ignored
        }
    }

    set doMove(func) {
        this._doMove = func
    }

    reset() {
        console.log('[Debug] Game#reset()');

        // Game board for maintaing the state of the game
        this.board = [
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
            PC_EMPTY, PC_EMPTY, PC_EMPTY,
        ];

        this.countOfMove = 0; // Number of moves done
        this.myTurn = true; // Boolean variable to get the turn of the player.
    }

    /**
     * Make a move
     * @param {number} sq - Square; 0 <= sq
     * @param {*} myPiece 
     * @returns 
     */
    makeMove(sq, myPiece){

        if(this.board[sq] == PC_EMPTY){
            // if the valid move, update the board
            // state and send the move to the server.
            this.countOfMove++;

            switch (myPiece) {
                case 'X':
                    this.board[sq] = 1;
                    break;
                case 'O':
                    this.board[sq] = 0;
                    break;
                default:
                    alert(`[Error] Invalid my piece = ${myPiece}`);
                    return false;
            }

            // Send
            engine1.protocol.sendDoMove(sq, myPiece)
        }

        // place the move in the game box.
        vue1.setLabelOfButton(sq, myPiece);

        // check for the winner
        const gameOver = this.isGameOver();
        if(this.myTurn){
            // if player winner, send the END event.
            if (gameOver) {
                // Send
                engine1.protocol.sendWon(myPiece)
            }
            else if (!gameOver && this.countOfMove == 9) {
                // Send
                engine1.protocol.sendDraw()
            }
        }
    }

    /**
     * function to check if player is winner.
     * @returns I won
     */
    isGameOver(){
        if (5 <= this.countOfMove) {
            for (let squaresOfWinPattern of WIN_PATTERN) {
                if (this.isPieceInLine(squaresOfWinPattern)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * check if their is winning move
     * @param {*} squaresOfWinPattern 
     * @returns 
     */
    isPieceInLine(squaresOfWinPattern) {
        return this.board[squaresOfWinPattern[0]] !== PC_EMPTY &&
            this.board[squaresOfWinPattern[0]] === this.board[squaresOfWinPattern[1]] &&
            this.board[squaresOfWinPattern[0]] === this.board[squaresOfWinPattern[2]];
    }
}
