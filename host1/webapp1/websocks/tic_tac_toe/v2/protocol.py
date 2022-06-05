class TicTacToeV2Protocol():
    """サーバープロトコル"""

    def execute(self, request):
        """サーバーからクライアントへ送信するメッセージの作成"""

        event = request.get("event", None)

        if event == 'CtoS_End':
            # 対局終了時

            self.on_end(request)

            return {
                'type': 'send_message',
                'event': "StoC_End",
                'winner': request.get("winner", None),
            }

        elif event == 'CtoS_Move':
            # 石を置いたとき

            self.on_move(request)

            return {
                'type': 'send_message',
                "event": "StoC_Move",
                'sq': request.get("sq", None),
                'myPiece': request.get("myPiece", None),
            }

        elif event == 'CtoS_Start':
            # 対局開始時

            self.on_start(request)

            return {
                'type': 'send_message',
                'event': "StoC_Start",
            }

        raise ValueError(f"Unknown event: {event}")

    def on_end(self, request):
        """対局終了時"""
        pass

    def on_move(self, request):
        """石を置いたとき"""
        pass

    def on_start(self, request):
        """対局開始時"""
        pass
