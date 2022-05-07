function protocol_setup() {
    connection1.setup((event, message) => {
        console.log(`[connection1.setup] event=${event}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "E_Start":
                vue1.reset();
                break;
            
            case "E_End":
                alert(`[Notice] ${message}`);
                vue1.reset();
                break;
            
            case "E_Move":
                if(message["player"] != connection1.myPiece){
                    game1.makeMove(parseInt(message["index"]), message["player"])
                    game1.myTurn = true;
                    document.getElementById("alert_your_move").style.display = 'block';
                }
                break;
            
            default:
                console.log("No event")
        }
    })
}
