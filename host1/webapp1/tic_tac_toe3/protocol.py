class Protocol():
    """サーバープロトコル"""

    def execute(self, response):
        """サーバーからクライアントへ送信するメッセージの作成"""

        event = response.get("event", None)

        if event == 'CtoS_End':
            # 対局終了時
            return {
                'type': 'send_message',
                'event': "StoC_End",
                'winner': response.get("winner", None),
            }

        elif event == 'CtoS_Move':
            # 石を置いたとき
            return {
                'type': 'send_message',
                "event": "StoC_Move",
                'sq': response.get("sq", None),
                'myPiece': response.get("myPiece", None),
            }

        elif event == 'CtoS_Start':
            # 対局開始時
            return {
                'type': 'send_message',
                'event': "StoC_Start",
            }

        raise ValueError(f"Unknown event: {event}")
