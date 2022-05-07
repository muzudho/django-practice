class Protocol {

    /**
     * if player winner, send the END event.
     */
    createWon(myPiece) {
        return {
            "event": "E_End",
            "message": `${myPiece} is a winner. Play again?`
        }
    }

    createDraw() {
        return {
            "event": "E_End",
            "message": "It's a draw. Play again?"
        }
    }

    createDoMove(sq, myPiece) {
        return {
            "event": "E_Move",
            "message":
            {
                "index": sq,
                "player": myPiece
            }
        }
    }

    createStart() {
        return {
            "event": "E_Start",
            "message": ""
        }
    }
}
