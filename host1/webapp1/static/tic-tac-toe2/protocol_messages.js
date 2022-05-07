class ProtocolMessages {

    /**
     * if player winner, send the END event.
     */
    createWon(myPiece) {
        return {
            "event": "E_End",
            "text": `${myPiece} is a winner. Play again?`
        }
    }

    createDraw() {
        return {
            "event": "E_End",
            "text": "It's a draw. Play again?"
        }
    }

    createDoMove(sq, myPiece) {
        return {
            "event": "E_Move",
            "sq": sq,
            "myPiece": myPiece,
        }
    }

    createStart() {
        return {
            "event": "E_Start",
        }
    }
}
