function protocol_setup() {
    connection1.setup((event, message) => {
        console.log(`[setRequest] event=${event} message=${message}`); // ちゃんと動いているようなら消す

        switch (event) {
            case "START":
                vue1.reset();
                break;
            
            case "END":
                alert(message);
                vue1.reset();
                break;
            
            case "MOVE":
                if(message["player"] != connection1.myPiece){
                    game1.makeMove(parseInt(message["index"]), message["player"])
                    game1.myTurn = true;
                    document.getElementById("alert_move").style.display = 'block';
                }
                break;
            
            default:
                console.log("No event")
        }
    })
}
