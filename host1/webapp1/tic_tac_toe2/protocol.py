class Protocol():

    def __init__(self):
        pass

    def execute(self, response):
        event = response.get("event", None)

        if event == 'CtoS_End':
            # 対局終了
            return {
                'type': 'send_message',
                'event': "StoC_End",
                'text': response.get("text", None),
            }

        elif event == 'CtoS_Move':
            # 石を置いた
            return {
                'type': 'send_message',
                "event": "StoC_Move",
                'sq': response.get("sq", None),
                'myPiece': response.get("myPiece", None),
            }

        elif event == 'CtoS_Start':
            # 対局開始
            return {
                'type': 'send_message',
                'event': "StoC_Start",
            }

        raise ValueError(f"Unknown event: {event}")
