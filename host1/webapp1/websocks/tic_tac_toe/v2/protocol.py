class TicTacToeV2Protocol():
    """サーバープロトコル"""

    def execute(self, doc_received, user):
        """サーバーからクライアントへ送信するメッセージの作成"""

        # ログインしていなければ AnonymousUser
        print(f"[TicTacToeV2Protocol execute] user=[{user}]")

        event = doc_received.get("event", None)

        if event == 'CtoS_End':
            # 対局終了時

            self.on_end(doc_received)

            return {
                'type': 'send_message',
                'event': "StoC_End",
                'winner': doc_received.get("winner", None),
            }

        elif event == 'CtoS_Move':
            # 石を置いたとき

            self.on_move(doc_received)

            return {
                'type': 'send_message',
                "event": "StoC_Move",
                'sq': doc_received.get("sq", None),
                'myPiece': doc_received.get("myPiece", None),
            }

        elif event == 'CtoS_Start':
            # 対局開始時

            self.on_start(doc_received)

            return {
                'type': 'send_message',
                'event': "StoC_Start",
            }

        raise ValueError(f"Unknown event: {event}")

    def on_end(self, doc_received):
        """対局終了時"""
        pass

    def on_move(self, doc_received):
        """石を置いたとき"""
        pass

    def on_start(self, doc_received):
        """対局開始時"""
        pass
