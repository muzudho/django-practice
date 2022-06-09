from webapp1.websocks.tic_tac_toe.v2.consumer_base import TicTacToeV2ConsumerBase
#                                  ^ two                            ^ two
#    ------- ----------------------- -------------        -----------------------
#    1       2                       3                    4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.websocks.tic_tac_toe.v3o1.protocol import TicTacToeV3o1Protocol
#                                  ^^^ three o one               ^ three o one
#    ------- ----------------------- ----------        ---------------------
#    1       2                       3                 4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV3o1ConsumerCustom(TicTacToeV2ConsumerBase):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()
        self._protocol = TicTacToeV3o1Protocol()
        #                          ^^^ three o one

    def on_receive(self, doc_received):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """

        # ログインしていなければ AnonymousUser
        user = self.scope["user"]
        print(f"[TicTacToeV3o1ConsumerCustom on_receive] user=[{user}]")
        return self._protocol.execute(doc_received, user)
