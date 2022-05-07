class Engine {
    constructor() {
        this._connection = new Connection();
        this._protocol = new Protocol();
    }

    get connection() {
        return this._connection
    }

    get protocol() {
        return this._protocol
    }
}