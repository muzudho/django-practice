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
}