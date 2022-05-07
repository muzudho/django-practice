class Protocol():

    def __init__(self):
        pass

    def execute(self, event, message):
        if event == 'E_End':
            # 対局終了
            return {
                'type': 'send_message',
                'event': "E_End",
                'message': message,
            }

        elif event == 'E_Move':
            # 石を置いた
            return {
                'type': 'send_message',
                "event": "E_Move",
                'message': message,
            }

        elif event == 'E_Start':
            # 対局開始
            return {
                'type': 'send_message',
                'event': "E_Start",
                'message': message,
            }

        raise ValueError(f"Unknown event: {event}")
