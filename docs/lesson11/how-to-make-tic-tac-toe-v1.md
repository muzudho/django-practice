# 目的

Webサーバーと、クライアント側のアプリ間で通信する練習をしたい。  
だから 〇×ゲーム（Tic tac toe）のサンプルプログラムを真似する。  
１人２役で２窓で遊ぶ。  

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key              | Value                                     |
| ---------------- | ----------------------------------------- |
| OS               | Windows10                                 |
| Container        | Docker                                    |
| Web framework    | Django                                    |
| Communication    | JSON                                      |
| Database         | Redis                                     |
| Program Language | Python 3                                  |
| Others           | Web socket                                |
| Editor           | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    ├── 📂sockapp1
    │    │   ├── 📄client.py
    │    │   ├── 📄echo_server.py
    │    │   └── 📄main_finally.py
    │    └── 📂websockapp1
    │        ├── 📄client2.py
    │        ├── 📄main_finally.py
    │        └── 📄websock_client.py
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   └── 📂vuetify-practice
        │   │       └── 📄desserts.json
        │   ├── 📂templates
        │   │   └── 📂<いろいろ>-practice
        │   │       └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂websock_practice1
        │   │       └── 📂v1
        │   │           └── 📄consumer.py
        │   ├── 📄admin.py
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── <いろいろ>
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── <いろいろ>
```

以下、参考にした元記事は 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

# Step 1. プログラミング環境更新 - requirements.txt ファイル

（無ければ）ファイルの末尾にでも追加してほしい。  

```plaintext
    └── 📂host1
👉      └── 📄requirements.txt
```

```shell
channels_redis>=3.2
```

# Step 2. コマンド実行

Dockerコンテナは停止しているものとし、以下のコマンドを打鍵してほしい。  

```shell
cd host1

# settings.py を編集したのでマイグレーションし直します
docker-compose run --rm web python3 manage.py migrate
#                       ---
#                       1
# 1. docker-compose.yml ファイルに書いてある services の子要素名

# 起動
docker-compose up
```

# Step 3. Web ページのスタイル作成 - main.css ファイル

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   └── 📂static
        │       └── 📂tic-tac-toe
        │           └── 📂v1
👉      │               └── 📄main.css
        └── 📄requirements.txt
```

```css
/* static/css/main.css */
body {
  /* width: 100%; */
  height: 90vh;
  background: #f1f1f1;
  display: flex;
  justify-content: center;
  align-items: center;
}
#board {
  display: grid;
  grid-gap: 0.5em;
  grid-template-columns: repeat(3, 1fr);
  width: 16em;
  height: auto;
  margin: 0.5em 0;
}
.square {
  background: #2f76c7;
  width: 5em;
  height: 5em;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 0.5em;
  font-weight: 500;
  color: white;
  box-shadow: 0.025em 0.125em 0.25em rgba(0, 0, 0, 0.25);
}
.head {
  width: 16em;
  text-align: center;
}
.wrapper h1,
h3 {
  color: #0a2c1a;
}
label {
  font-size: 20px;
  color: #0a2c1a;
}
input,
select {
  margin-bottom: 10px;
  width: 100%;
  padding: 15px;
  border: 1px solid #125a33;
  font-size: 14px;
  background-color: #71d19e;
  color: white;
}
.button {
  color: white;
  white-space: nowrap;
  background-color: #31d47d;
  padding: 10px 20px;
  border: 0;
  border-radius: 2px;
  transition: all 150ms ease-out;
}
```

# Step 4. play.js ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   └── 📂static
        │       └── 📂tic-tac-toe
        │           └── 📂v1
👉      │               ├── 📄play.js
        │               └── 📄main.css
        └── 📄requirements.txt
```

```js
// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

var roomName = document.getElementById("board").getAttribute("room_name");
var myPiece = document.getElementById("board").getAttribute("my_piece");

var connectionString = `ws://${window.location.host}/tic-tac-toe/v1/${roomName}/`;
//                           ----------------------- ---------------------------
//                           1                       2
// 1. ホスト アドレス
// 2. URLの一部

var webSock1 = new WebSocket(connectionString);

const PC_EMPTY = -1 // A square without piece; PC is piece
// Game board for maintaing the state of the game
var board = [
    PC_EMPTY, PC_EMPTY, PC_EMPTY,
    PC_EMPTY, PC_EMPTY, PC_EMPTY,
    PC_EMPTY, PC_EMPTY, PC_EMPTY,
];

// SQ is square
// +---------+
// | 0  1  2 |
// | 3  4  5 |
// | 6  7  8 |
// +---------+
const SQ_0 = 0
const SQ_1 = 1
const SQ_2 = 2
const SQ_3 = 3
const SQ_4 = 4
const SQ_5 = 5
const SQ_6 = 6
const SQ_7 = 7
const SQ_8 = 8
// Winning indexes.
arrayOfSquaresOfWinPattern = [
    // +---------+
    // | *  *  * |
    // | .  .  . |
    // | .  .  . |
    // +---------+
    [SQ_0, SQ_1, SQ_2],
    // +---------+
    // | .  .  . |
    // | *  *  * |
    // | .  .  . |
    // +---------+
    [SQ_3, SQ_4, SQ_5],
    // +---------+
    // | .  .  . |
    // | .  .  . |
    // | *  *  * |
    // +---------+
    [SQ_6, SQ_7, SQ_8],
    // +---------+
    // | *  .  . |
    // | *  .  . |
    // | *  .  . |
    // +---------+
    [SQ_0, SQ_3, SQ_6],
    // +---------+
    // | .  *  . |
    // | .  *  . |
    // | .  *  . |
    // +---------+
    [SQ_1, SQ_4, SQ_7],
    // +---------+
    // | .  .  * |
    // | .  .  * |
    // | .  .  * |
    // +---------+
    [SQ_2, SQ_5, SQ_8],
    // +---------+
    // | *  .  . |
    // | .  *  . |
    // | .  .  * |
    // +---------+
    [SQ_0, SQ_4, SQ_8],
    // +---------+
    // | .  .  * |
    // | .  *  . |
    // | *  .  . |
    // +---------+
    [SQ_2, SQ_4, SQ_6]
]
let countOfMove = 0; // Number of moves done
let myTurn = true; // Boolean variable to get the turn of the player.

// Add the click event listener on every block.
let elementArrayOfSquare = document.getElementsByClassName('square');
for (const element of elementArrayOfSquare) {
    element.addEventListener("click", event=>{
        const sq = event.path[0].getAttribute('square'); // Square; 0 <= sq
        if(board[sq] == PC_EMPTY){
            if(!myTurn){
                alert("Wait for other to place the move")
            }
            else{
                myTurn = false;
                document.getElementById("alert_move").style.display = 'none'; // Hide
                makeMove(sq, myPiece);
            }
        }
    })
}

/**
 * Make a move
 * @param {*} sq - Square; 0 <= sq
 * @param {*} myPiece 
 * @returns 
 */
function makeMove(sq, myPiece){
    sq = parseInt(sq);
    let data = {
        "event": "MOVE",
        "message": {
            "index": sq,
            "player": myPiece
        }
    }

    if(board[sq] == PC_EMPTY){
        // if the valid move, update the board
        // state and send the move to the server.
        countOfMove++;

        switch (myPiece) {
            case 'X':
                board[sq] = 1;
                break;
            case 'O':
                board[sq] = 0;
                break;
            default:
                alert(`Invalid my piece = ${myPiece}`);
                return false;
        }

        webSock1.send(JSON.stringify(data))
    }
    // place the move in the game box.
    elementArrayOfSquare[sq].innerHTML = myPiece;
    // check for the winner
    const gameOver = isGameOver();
    if(myTurn){
        // if player winner, send the END event.
        if(gameOver){
            data = {
                "event": "END",
                "message": `${myPiece} is a winner. Play again?`
            }
            webSock1.send(JSON.stringify(data))
        }
        else if(!gameOver && countOfMove == 9){
            data = {
                "event": "END",
                "message": "It's a draw. Play again?"
            }
            webSock1.send(JSON.stringify(data))
        }
    }
}

// function to reset the game.
function reset(){
    board = [
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
        PC_EMPTY, PC_EMPTY, PC_EMPTY,
    ];
    countOfMove = 0;
    myTurn = true;
    document.getElementById("alert_move").style.display = 'inline';
    for (const element of elementArrayOfSquare) {
        element.innerHTML = "";
    }
}

/**
 * check if their is winning move
 * @param {*} squaresOfWinPattern 
 * @returns 
 */
function isPieceInLine(squaresOfWinPattern) {
    return board[squaresOfWinPattern[0]] !== PC_EMPTY &&
        board[squaresOfWinPattern[0]] === board[squaresOfWinPattern[1]] &&
        board[squaresOfWinPattern[0]] === board[squaresOfWinPattern[2]];
}

/**
 * function to check if player is winner.
 * @returns I won
 */
function isGameOver(){
    if (5 <= countOfMove) {
        for (let squaresOfWinPattern of arrayOfSquaresOfWinPattern) {
            if (isPieceInLine(squaresOfWinPattern)) {
                return true;
            }
        }
    }
    return false;
}

/**
 * Main function which handles the connection
 * of websocket.
 */
function connect() {
    // on websocket open, send the START event.
    webSock1.onopen = () => {
        console.log('WebSockets connection created.');
        webSock1.send(JSON.stringify({
            "event": "START",
            "message": ""
        }));
    };

    webSock1.onclose = (e) => {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };

    // Sending the info about the room
    webSock1.onmessage = (e) => {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        data = data["payload"];
        let message = data['message'];
        let event = data["event"];
        switch (event) {
            case "START":
                console.log(`[Message] START e=${e.data}`); // ちゃんと動いているようなら消す
                reset();
                break;
            case "END":
                console.log(`[Message] END e=${e.data}`); // ちゃんと動いているようなら消す
                alert(message);
                reset();
                break;
            case "MOVE":
                console.log(`[Message] MOVE e=${e.data}`); // ちゃんと動いているようなら消す
                if(message["player"] != myPiece){
                    makeMove(message["index"], message["player"])
                    myTurn = true;
                    document.getElementById("alert_move").style.display = 'inline';
                }
                break;
            default:
                console.log(`[Message] (Others) e=${e.data}`); // ちゃんと動いているようなら消す
                console.log("No event")
        }
    };

    if (webSock1.readyState == WebSocket.OPEN) {
        console.log('Open socket.');
        webSock1.onopen();
    }
}

//call the connect function at the start.
connect();
```

# Step 5. entry.html ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   └── 📂templates
        │       └── 📂tic-tac-toe
        │           └── 📂v1
👉      │               └── 📄entry.html
        └── 📄requirements.txt
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Tic Tac Toe</title>
        <link rel="stylesheet" href='{% static "/tic-tac-toe/v1/main.css" %}' />
    </head>
    <body>
        <div class="wrapper">
            <h1>Welcome to Tic Tac Toe Game</h1>
            <form method="POST">
                {% csrf_token %}
                <div class="form-control">
                    <label for="room">Room id</label>
                    <input id="room" type="text" name="room_name" required />
                </div>
                <div class="form-control">
                    <label for="item_of_my_piece">Your character</label>
                    <select for="item_of_my_piece" name="my_piece">
                        <option value="X">X</option>
                        <option value="O">O</option>
                    </select>
                </div>
                <input type="submit" class="button" value="Start Game" />
            </form>
        </div>
    </body>
</html>
```

# Step 6. play.html ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   └── 📂templates
        │       └── 📂tic-tac-toe
        │           └── 📂v1
👉      │               ├── 📄play.html
        │               └── 📄entry.html
        └── 📄requirements.txt
```

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Tic Tac Toe</title>
        <link rel="stylesheet" href='{% static "/tic-tac-toe/v1/main.css" %}' />
    </head>
    <body>
        <div class="wrapper">
            <div class="head">
                <h1>TIC TAC TOE</h1>
                <h3>Welcome to room_{{room_name}}</h3>
            </div>
            <div id="board" room_name="{{room_name}}" my_piece="{{my_piece}}">
                <div class="square" square="0"></div>
                <div class="square" square="1"></div>
                <div class="square" square="2"></div>
                <div class="square" square="3"></div>
                <div class="square" square="4"></div>
                <div class="square" square="5"></div>
                <div class="square" square="6"></div>
                <div class="square" square="7"></div>
                <div class="square" square="8"></div>
            </div>
            <div id="alert_move">Your turn. Place your move <strong>{{my_piece}}</strong></div>
        </div>

        <script src="{% static 'tic-tac-toe/v1/play.js' %}"></script>
        {% block javascript %} {% endblock javascript %}
    </body>
</html>
```

# Step 7. ビュー編集 - v_tic_tac_toe_v1.py ファイル

以下のファイルが既存なら編集を、無ければ新規作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   ├── 📂templates
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.html
        │   │           └── 📄entry.html
        │   └── 📂views
👉      │       └── 📄v_tic_tac_toe_v1.py
        └── 📄requirements.txt
```

```py
from django.http import Http404
from django.shortcuts import render, redirect


def visitEntry(request):
    """エントリー画面"""
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        return redirect(f'/tic-tac-toe/v1/{room_name}/?&mypiece={myPiece}')
        #                 -----------------------------------------------
        #                 1
        # 1. http://example.com:8000/tic-tac-toe/v1/Elephant/?&mypiece=X
        #                           ------------------------------------
    return render(request, "tic-tac-toe/v1/entry.html", {})
    #                       -------------------------
    #                       1
    # 1. webapp1/templates/tic-tac-toe/v1/entry.html
    #                      -------------------------


def visitPlay(request, room_name):
    """対局画面"""
    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")
    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, "tic-tac-toe/v1/play.html", context)
    #                       ------------------------
    #                       1
    # 1. webapp1/templates/tic-tac-toe/v1/play.html
    #                      ------------------------
```

# Step 8. ルート編集 - urls.py ファイル

📄`urls.py` は既存だろうから、以下のソースをマージしてほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   ├── 📂templates
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.html
        │   │           └── 📄entry.html
        │   ├── 📂views
        │   │   └── 📄v_tic_tac_toe_v1.py
👉      │   └── 📄urls.py
        └── 📄requirements.txt
```

```py
from django.urls import path

from webapp1.views import v_tic_tac_toe_v1
#    ------- -----        ----------------
#    1       2            3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き

urlpatterns = [
    # ...略...

    # 〇×ゲームの練習１
    path('tic-tac-toe/v1/', v_tic_tac_toe_v1.visitEntry),
    #     ---------------   ---------------------------
    #     1                 2
    # 1. URLの `tic-tac-toe/v1/` というパスにマッチする
    # 2. v_tic_tac_toe_v1.py ファイルの visitEntry メソッド

    # 〇×ゲームの練習１
    path('tic-tac-toe/v1/<str:room_name>/', v_tic_tac_toe_v1.visitPlay),
    #     -------------------------------   --------------------------
    #     1                                 2
    # 1. URLの `tic-tac-toe/v1/<部屋名>/` というパスにマッチする。 <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. v_tic_tac_toe_v1.py ファイルの visitPlay メソッド
]
```

# Step 9. consumer.py ファイルの作成

以下のファイルを作成してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   ├── 📂templates
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.html
        │   │           └── 📄entry.html
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       └── 📂v1
👉      │   │           └── 📄consumer.py
        │   ├── 📂views
        │   │   └── 📄v_tic_tac_toe_v1.py
        │   └── 📄urls.py
        └── 📄requirements.txt
```

```py
# See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TicTacToeV1Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        print(
            f"[Debug] Consumer1 receive text_data={text_data}")  # ちゃんと動いているようなら消す
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
```

# Step 10. ルート編集 - routing1.py ファイル

以下のファイルを無ければ作成、あればマージしてほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   ├── 📂templates
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.html
        │   │           └── 📄entry.html
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       └── 📂v1
        │   │           └── 📄consumer.py
        │   ├── 📂views
        │   │   └── 📄v_tic_tac_toe_v1.py
👉      │   ├── 📄routing1.py
        │   └── 📄urls.py
        └── 📄requirements.txt
```

```py
from django.conf.urls import url

# 〇×ゲームの練習１
from webapp1.websocks.tic_tac_toe.v1.consumer import TicTacToeV1Consumer
#    ------- ----------------------- --------        -------------------
#    1       2                       3                4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

websocket_urlpatterns = [
    # ...中略...

    # 〇×ゲームの練習１
    url(r'^tic-tac-toe/v1/(?P<room_name>\w+)/$', TicTacToeV1Consumer.as_asgi()),
    #     ------------------------------------   -----------------------------
    #     1                                      2
    # 1. URLのパスの部分の、Django での正規表現の書き方
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
```

# Step 11. 設定の編集 - asgi.py ファイル

無ければ以下のファイルを作成、あればマージしてほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1
        │   ├── 📂static
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.js
        │   │           └── 📄main.css
        │   ├── 📂templates
        │   │   └── 📂tic-tac-toe
        │   │       └── 📂v1
        │   │           ├── 📄play.html
        │   │           └── 📄entry.html
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       └── 📂v1
        │   │           └── 📄consumer.py
        │   ├── 📂views
        │   │   └── 📄v_tic_tac_toe_v1.py
👉      │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   └── 📄urls.py
        └── 📄requirements.txt
```

```py
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import webapp1.routing1
#      ------- --------
#      1       2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp1.settings')
#                                                -------
#                                                1
# 1. アプリケーション フォルダー名

# （削除） application = get_asgi_application()
application = ProtocolTypeRouter({ # 追加
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            webapp1.routing1.websocket_urlpatterns
            # -----
            # 1
            #
            # 1. アプリケーション フォルダー名
        )
    ),
})
```

# Step 12. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください。  

📖 [http://localhost:8000/tic-tac-toe/v1/](http://localhost:8000/tic-tac-toe/v1/)  

# 次の記事

📖 [Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！ Vuetify編](https://qiita.com/muzudho1/items/f302bdb40fb5c13f9603)

# 参考にした記事

📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  
