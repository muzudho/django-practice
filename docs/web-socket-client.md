📖 [Python WebSocket通信の仕方：クライアント編](https://www.raspberrypirulo.net/entry/websocket-client)  

# Step 1. ローカルPCにインストール

あなたのPCでコマンドを打鍵してほしい。  

```shell
pip install websocket-client
```

# Step 2. websock_client.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
├── 📂host_local1
│    ├── 📂sockapp1
│    └── 📂websockapp1
│        └── 📄websock_client.py # ここに新規作成
└── 📂host1                      # 既存
         ├── 📂data
         ├── 📂webapp1
         └── <いろいろ>
```

📄`host_local1/websockapp1/websock_client.py`:  

```py
# See also: 📖 [Python WebSocket通信の仕方：クライアント編](https://www.raspberrypirulo.net/entry/websocket-client)
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

class Websocket_Client():

    def __init__(self, host_addr):

        # デバックログの表示/非表示設定
        websocket.enableTrace(True)

        # WebSocketAppクラスを生成
        # 関数登録のために、ラムダ式を使用
        self.ws = websocket.WebSocketApp(host_addr,
            on_message = lambda ws, msg: self.on_message(ws, msg),
            on_error   = lambda ws, msg: self.on_error(ws, msg),
            on_close   = lambda ws: self.on_close(ws))
        self.ws.on_open = lambda ws: self.on_open(ws)

    # メッセージ受信に呼ばれる関数
    def on_message(self, ws, message):
        print("receive : {}".format(message))

    # エラー時に呼ばれる関数
    def on_error(self, ws, error):
        print(error)

    # サーバーから切断時に呼ばれる関数
    def on_close(self, ws):
        print("### closed ###")

    # サーバーから接続時に呼ばれる関数
    def on_open(self, ws):
        thread.start_new_thread(self.run, ())

    # サーバーから接続時にスレッドで起動する関数
    def run(self, *args):
        while True:
            time.sleep(0.1)
            input_data = input("send data:") 
            self.ws.send(input_data)

        self.ws.close()
        print("thread terminating...")

    # websocketクライアント起動
    def run_forever(self):
        self.ws.run_forever()


HOST_ADDR = "ws://192.168.1.10:9001/"
ws_client = Websocket_Client(HOST_ADDR)
ws_client.run_forever()
```

# Step 3. コマンド実行

```shell
cd host_local1/websockapp1

python.exe -m websock_client
```
