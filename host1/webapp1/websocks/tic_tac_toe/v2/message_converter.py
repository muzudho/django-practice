class TicTacToeV2MessageConverter():
    """サーバープロトコル"""

    async def on_receive(self, doc_received, user):
        """クライアントからサーバーへ送られてきた変数を解析し、
        サーバーからクライアントへ送信するメッセージの作成"""

        # `c2s_` は クライアントからサーバーへ送られてきた変数の目印
        event = doc_received.get("c2s_event", None)

        # ログインしていなければ AnonymousUser
        print(
            f"[TicTacToeV2MessageConverter on_receive] user=[{user}] event=[{event}]")

        if event == 'C2S_End':
            # 対局終了時

            self.on_end(doc_received)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': "S2C_End",
                's2c_winner': doc_received.get("c2s_winner", None),
            }

        elif event == 'C2S_Move':
            # 石を置いたとき

            await self.on_move(doc_received, user)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                "s2c_event": "S2C_Move",
                's2c_sq': doc_received.get("c2s_sq", None),
                's2c_myPiece': doc_received.get("c2s_myPiece", None),
            }

        elif event == 'C2S_Start':
            # 対局開始時

            self.on_start(doc_received)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': "S2C_Start",
            }

        raise ValueError(f"Unknown event: {event}")

    def on_end(self, doc_received):
        """対局終了時"""
        print("[TicTacToeV2MessageConverter on_end] ignored")
        pass

    async def on_move(self, doc_received, user):
        """石を置いたとき"""
        print("[TicTacToeV2MessageConverter on_move] ignored")
        pass

    def on_start(self, doc_received):
        """対局開始時"""
        print("[TicTacToeV2MessageConverter on_start] ignored")
        pass
