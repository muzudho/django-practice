import sys
import traceback
import socket
import argparse
from threading import Thread
from main_finally import MainFinally


class Client:
    def __init__(self, server_host="127.0.0.1", server_port=5002, message_size=1024):
        """クライアントです。

        Parameters
        ----------
        server_host : str
            接続先サーバーのホスト名、またはIPアドレスです。 規定値 "127.0.0.1"

        server_port : int
            接続先サーバーのポート番号です。 規定値 5002

        message_size : int
            １回の通信で送れるバイト長。 規定値 1024
        """
        self._s_host = server_host
        self._s_port = server_port
        self._message_size = message_size

        # (Server socket) 接続先サーバーのソケットです
        self._s_sock = None

        # (Server thread) サーバーからのメッセージを受信するスレッド
        self._s_thr = None

        # サーバースレッドが終了したら、メインスレッドも終了させるのに使います
        self._is_terminate_server_thread = False

    def clean_up(self):
        # サーバーのソケットを閉じます
        self._s_sock.close()

        # 実行中のスレッドがあれば終了するまで待機するのがクリーンです
        if not (self._s_thr is None) and self._s_thr.is_alive():
            print("[CleanUp] Before join")
            self._s_thr.join()
            print("[CleanUp] After join")
            self._s_thr = None

    def run(self):
        def server_worker():
            while True:
                try:
                    message = self._s_sock.recv(self._message_size).decode()
                    print("\n" + message)

                    if message == "quit":
                        # サーバーから quit が送られてきたら終了することにします
                        # サーバーから強制的に切断しても同じですが、エラーメッセージが出ないという違いがあります
                        # TODO ただし、このワーカースレッドが止まっても、標準入力の待機からは自動的には抜けません
                        print(f"""[-] Disconnected by server.""")
                        self._is_terminate_server_thread = True
                        return

                except Exception as e:
                    # client no longer connected
                    # remove it from the set
                    print(f"[!] Error: {e}")

                    print(
                        f"""Finished listening to the server.
Please push q key to quit."""
                    )
                    self._is_terminate_server_thread = True
                    return

        # initialize TCP socket
        self._s_sock = socket.socket()
        # connect to the server
        print(f"[*] Connecting to {self._s_host}:{self._s_port}...")
        self._s_sock.connect((self._s_host, self._s_port))
        print("[+] Connected.")

        # make a thread that listens for messages to this client & print them
        self._s_thr = Thread(target=server_worker)
        # make the thread daemon so it ends whenever the main thread ends
        self._s_thr.daemon = True
        # start the thread
        self._s_thr.start()

        while not self._is_terminate_server_thread:
            # input message we want to send to the server
            to_send = input()  # ここでブロックします。このブロックをプログラムから解除する簡単な方法はありません

            # a way to exit the program
            if to_send.lower() == "q":
                break

            to_send = f"{to_send}"
            # finally, send the message
            self._s_sock.send(to_send.encode())

# このファイルを直接実行したときは、以下の関数を呼び出します
if __name__ == "__main__":

    class Main1:
        def __init__(self):
            self._client = None

        def on_main(self):
            parser = argparse.ArgumentParser(
                description='サーバーのアドレスとポートを指定して、テキストを送信します')
            parser.add_argument('--host', default="127.0.0.1", help='サーバーのホスト。規定値:127.0.0.1')
            parser.add_argument('--port', type=int, default=5002, help='サーバーのポート。規定値:5002')
            args = parser.parse_args()

            self._client = Client(server_host=args.host, server_port=args.port)
            self._client.run()
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
