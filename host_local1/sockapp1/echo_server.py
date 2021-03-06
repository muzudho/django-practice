# See also: ð [How to Make a Chat Application in Python](https://www.thepythoncode.com/article/make-a-chat-room-application-in-python)
import sys
import traceback
import socket
from threading import Thread
from main_finally import MainFinally


class EchoServer():
    def __init__(self, host="0.0.0.0", port=5002, message_size=1024):
        """åæå

        Parameters
        ----------
        host : str
            ãµã¼ãã¼ã®IPã¢ãã¬ã¹ã è¦å®å¤ "0.0.0.0"

        port : int
            ãµã¼ãã¼å´ã®ãã¼ãçªå·ã è¦å®å¤ 5002

        message_size : int
            ï¼åã®éä¿¡ã§éãããã¤ãé·ã è¦å®å¤ 1024
        """
        self._host = host
        self._port = port
        self._message_size = message_size

        # (Server socket) ãã®ãµã¼ãã¼ã®TCPã½ã±ããã§ã
        self._s_sock = None

        # (Client socket set) ãã®ãµã¼ãã¼ã«æ¥ç¶ãã¦ããã¯ã©ã¤ã¢ã³ãã®ã½ã±ããã®éã¾ãã§ã
        self._c_sock_set = None

    def run(self):
        def client_worker(c_sock):
            """ã¯ã©ã¤ã¢ã³ãããéä¿¡ããã¦ãããã¤ããªãã¼ã¿ã«å¯¾å¿ãã¾ã

            Parameters
            ----------
            c_sock : socket
                æ¥ç¶ãã¦ããã¯ã©ã¤ã¢ã³ãã®ã½ã±ãã
            """
            while True:
                try:
                    # ã¯ã©ã¤ã¢ã³ãããåä¿¡ãããã¤ããªãã¼ã¿ããã­ã¹ãã«å¤æãã¾ã
                    message = c_sock.recv(self._message_size).decode()

                    # ã¨ãããã "Echo: " ã¨é ­ã«ä»ãã¦ãã¤ããªãã¼ã¿ã«å¤æãã¦éãè¿ãã¾ã
                    message = f"Echo: {message}"
                    c_sock.send(message.encode())

                except Exception as e:
                    # client no longer connected
                    # remove it from the set
                    print(f"[!] Error: {e}")

                    print(f"Remove a socket")
                    self._c_sock_set.remove(c_sock)
                    break

        self._c_sock_set = set()  # åæå

        s_sock = socket.socket()  # ãã®ãµã¼ãã¼ã®TCPã½ã±ããã®è¨­å®ãè¡ã£ã¦ããã¾ã

        # make the port as reusable port
        s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # ãã¹ãã¨ãã¼ãçªå·ãè¨­å®ãã¾ã
        s_sock.bind((self._host, self._port))

        # ã¯ã©ã¤ã¢ã³ãã®åææ¥ç¶æ°ä¸é
        s_sock.listen(5)
        self._s_sock = s_sock

        print(f"[*] Listening as {self._host}:{self._port}")

        # ã¯ã©ã¤ã¢ã³ãããã®æ¥ç¶ãå¾ã¡ç¶ããã«ã¼ãã§ã
        while True:
            print(f"Wait a connection")
            # ã¯ã©ã¤ã¢ã³ãããã®æ¥ç¶ãããã¾ã§ãããã§ãã­ãã¯ãã¾ã
            # 'c_sock' - Client socket
            # 'c_addr' - Client address
            c_sock, c_addr = self._s_sock.accept()
            print(f"[+] {c_addr} connected.")

            # ã¯ã©ã¤ã¢ã³ãã®æ¥ç¶ãè¦ãã¦ããã¾ã
            self._c_sock_set.add(c_sock)

            # å¥ã¹ã¬ãããéå§ãã¾ã
            thr = Thread(target=client_worker, args=(c_sock,))

            # make the thread daemon so it ends whenever the main thread ends
            thr.daemon = True

            # start the thread
            thr.start()

    def clean_up(self):
        # ã¯ã©ã¤ã¢ã³ãã®ã½ã±ãããéãã¾ã
        print("Clean up")
        if not (self._c_sock_set is None):
            for c_sock in self._c_sock_set:
                c_sock.close()

        # ãµã¼ãã¼ã®ã½ã±ãããéãã¾ã
        if not (self._s_sock is None):
            self._s_sock.close()

# ãã®ãã¡ã¤ã«ãç´æ¥å®è¡ããã¨ãã¯ãä»¥ä¸ã®é¢æ°ãå¼ã³åºãã¾ã
if __name__ == "__main__":

    class Main1:
        def __init__(self):
            self._echo_server = None

        def on_main(self):
            self._echo_server = EchoServer(host="0.0.0.0", port=5002)
            self._echo_server.run()
            return 0

        def on_except(self, e):
            """ããã§ä¾å¤ã­ã£ãã"""
            traceback.print_exc()

        def on_finally(self):
            # [Ctrl] + [C] ãåãä»ããªããããããã«ããã®ã¯é£ãã
            if self._echo_server:
                self._echo_server.clean_up()

            print("âããã§çµãã")
            return 1

    sys.exit(MainFinally.run(Main1()))
