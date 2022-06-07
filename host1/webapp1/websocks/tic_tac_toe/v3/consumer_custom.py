from webapp1.websocks.tic_tac_toe.v2.consumer_base import TicTacToeV2ConsumerBase
#                                  ^ two                            ^ two
#    ------- ----------------------- -------------        -----------------------
#    1       2                       3                    4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.websocks.tic_tac_toe.v3.protocol import TicTacToeV3Protocol
#                                  ^ three                     ^ three
#    ------- ----------------------- --------        -------------------
#    1       2                       3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class TicTacToeV2ConsumerCustom(TicTacToeV2ConsumerBase):
    """Webソケット用コンシューマー"""

    def __init__(self):
        super().__init__()
        self._protocol = TicTacToeV3Protocol()

    def on_receive(self, request):
        """クライアントからメッセージを受信したとき

        Returns
        -------
        response
        """
        return self._protocol.execute(request)
