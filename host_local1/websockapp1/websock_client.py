# See also:
#     📖 [Python WebSocket通信の仕方：クライアント編](https://www.raspberrypirulo.net/entry/websocket-client)
#     📖 [websocket-client - Examples](https://websocket-client.readthedocs.io/en/latest/examples.html)
#     📖 [GitHub - websocket-client](https://github.com/websocket-client/websocket-client)
import sys
import traceback
import websocket

try:
    import thread # 見つからない
except ImportError:
    import _thread as thread # websocket-client の GitHub ではこっちが使われている

import time
import argparse
from main_finally import MainFinally

class Websocket_Client():

    def __init__(self, url):

        # デバックログの表示/非表示設定
        websocket.enableTrace(True)

        # WebSocketAppクラスを生成
        self.websockApp = websocket.WebSocketApp(url,
            on_open     = lambda ws: self.on_open(ws),
            on_close    =lambda ws, close_status_code, close_msg: self.on_close(ws, close_status_code, close_msg),
            on_message  = lambda ws, msg: self.on_message(ws, msg),
            on_error    = lambda ws, msg: self.on_error(ws, msg))


    def on_message(self, ws, message):
        """メッセージ受信に呼ばれる関数"""
        print("receive : {}".format(message))

    def on_error(self, ws, error):
        """エラー時に呼ばれる関数"""
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        """サーバーから切断時に呼ばれる関数"""
        print("### closed ###")

    def on_open(self, ws):
        """サーバーから接続時に呼ばれる関数"""
        thread.start_new_thread(self.run_worker, ())

    def run_worker(self, *args):
        """サーバーから接続時にスレッドで起動する関数"""
        while True:
            time.sleep(0.1)
            input_data = input("send data:") 
            self.websockApp.send(input_data)

    def clean_up(self):
        self.websockApp.close()
        print("thread terminating...")

    def run_forever(self):
        """websocketクライアント起動"""
        self.websockApp.run_forever()

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    class Main1:
        def __init__(self):
            self._client = None

        def on_main(self):
            parser = argparse.ArgumentParser(
                description='サーバーのアドレスとポートを指定して、テキストを送信します')
            parser.add_argument('--host', default="127.0.0.1", help='サーバーのホスト。規定値:127.0.0.1')
            parser.add_argument('--port', type=int, default=8000, help='サーバーのポート。規定値:8000')
            args = parser.parse_args()

            url = f"ws://{args.host}:{args.port}/websock1/"
            self._client = Websocket_Client(url)
            self._client.run_forever()
            return 0

        def on_except(self, e):
            """ここで例外キャッチ"""
            traceback.print_exc()

        def on_finally(self):
            if self._client:
                self._client.clean_up()

            print("★これで終わり")
            return 1

    sys.exit(MainFinally.run(Main1()))
