class Engine {
    constructor() {
        this._connection = new Connection();
        this._protocol = new Protocol();
        this._game = new Game();
    }

    get connection() {
        return this._connection
    }

    get protocol() {
        return this._protocol
    }

    get game() {
        return this._game
    }

    setup() {
        this.protocol.setup();

        // １手進めたとき
        this.game.onDoMove = (sq, myPiece) => {
            this.protocol.sendDoMove(sq, myPiece)
        }

        // どちらかが勝ったとき
        this.game.onWon = (myPiece) => {
            this.protocol.sendWon(myPiece)
        }

        // 引き分けたとき
        this.game.onDraw = () => {
            this.protocol.sendDraw()
        }
    }
}