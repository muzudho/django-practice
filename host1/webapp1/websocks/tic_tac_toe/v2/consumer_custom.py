from webapp1.websocks.tic_tac_toe.v2.consumer_base import TicTacToeV2ConsumerBase
#                                  ^ two                            ^ two
#    ------- ----------------------- -------------        -----------------------
#    1       2                       3                    4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.websocks.tic_tac_toe.v2.message_converter import TicTacToeV2MessageConverter
#                                  ^ two                                ^ two
#    ------- ----------------------- -----------------        ---------------------------
#    1       2                       3                        4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV2ConsumerCustom(TicTacToeV2ConsumerBase):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()
        self._messageConverter = TicTacToeV2MessageConverter()

    async def on_receive(self, doc_received):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """

        # ログインしていなければ AnonymousUser
        user = self.scope["user"]
        print(f"[TicTacToeV2ConsumerCustom on_receive] user=[{user}]")
        return await self._messageConverter.on_receive(doc_received, user)
