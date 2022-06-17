class TicTacToeV2MessageConverter():
    """サーバープロトコル"""

    async def on_receive(self, scope, doc_received):
        """クライアントからサーバーへ送られてきた変数を解析し、
        サーバーからクライアントへ送信するメッセージの作成"""

        # ログインしていなければ AnonymousUser
        user = scope["user"]
        print(f"[TicTacToeV2MessageConverter on_receive] user=[{user}]")

        # `c2s_` は クライアントからサーバーへ送られてきた変数の目印
        event = doc_received.get("c2s_event", None)

        if event == 'C2S_End':
            # 対局終了時
            print(f"[TicTacToeV2MessageConverter on_receive] C2S_End")

            self.on_end(scope, doc_received)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': "S2C_End",
                # TODO 現状、クライアント側から勝者を送ってきているが、勝敗判定のロジックはサーバー側に置きたい
                's2c_winner': doc_received.get("c2s_winner", None),
            }

        elif event == 'C2S_Moved':
            # 駒を置いたとき
            # `s2c_` は サーバーからクライアントへ送る変数の目印
            c2s_sq = doc_received.get("c2s_sq", None)
            piece_moved = doc_received.get("c2s_pieceMoved", None)
            print(
                f"[TicTacToeV2MessageConverter on_receive] C2S_Moved c2s_sq=[{c2s_sq}] piece_moved=[{piece_moved}]")

            await self.on_move(scope, doc_received)

            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': 'S2C_Moved',
                's2c_sq': c2s_sq,
                's2c_pieceMoved': piece_moved,
            }

        elif event == 'C2S_Start':
            # 対局開始時
            print(f"[TicTacToeV2MessageConverter on_receive] C2S_Start")

            self.on_start(scope, doc_received)

            # `s2c_` は サーバーからクライアントへ送る変数の目印
            return {
                'type': 'send_message',  # type属性は必須
                's2c_event': "S2C_Start",
            }

        raise ValueError(f"Unknown event: {event}")

    def on_end(self, scope, doc_received):
        """対局終了時"""
        # print("[TicTacToeV2MessageConverter on_end] ignored")
        pass

    async def on_move(self, scope, doc_received):
        """駒を置いたとき"""
        # print("[TicTacToeV2MessageConverter on_move] ignored")
        pass

    def on_start(self, scope, doc_received):
        """対局開始時"""
        # print("[TicTacToeV2MessageConverter on_start] ignored")
        pass
