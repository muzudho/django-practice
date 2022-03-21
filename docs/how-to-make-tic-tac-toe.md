# 目的

Webサーバーと、クライアント側のアプリ間で通信する練習をしたい。  
だから 〇×ゲーム（Tic tac toe）を作る方法を説明する。  

# はじめに

この連載の最初のページ: 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

前提知識:  

| Key                                                                                 | Value                                                                                                                                     |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Webサーバーとクライアント側のアプリ間でJSON形式のテキストで通信する方法を知っておく | 📖[DjangoのWebサーバーとクライアント側のアプリ間でJSON形式のテキストを通信しよう！](https://qiita.com/muzudho1/items/a3870c78f609a65debe0) |

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

参考にした元記事は 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

前の記事から続いていて、ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
├── 📂host_local1
│    └── 📂websockapp1
│        ├── 📄client2.py
│        ├── 📄main_finally.py
│        └── 📄websock_client.py
└── 📂host1
     ├── 📂data
     │　　└── 📂db
     │         └── <たくさんのもの>
     ├── 📂webapp1
     │　　├── 📂templates
     │　　├── 📂websock1
     │　　│    ├── consumer1.py
     │　　│    └── consumer2.py
     │　　├── 📄asgi.py
     │　　├── 📄models.py
     │　　├── 📄routing1.py
     │　　├── 📄settings.py
     │　　├── 📄urls.py
     │　　└── <いろいろ>
     ├── 📄.env
     ├── 🐳docker-compose.yml
     ├── 🐳Dockerfile
     ├── 📄manage.py
     ├── 📄requirements.txt
     └── <いろいろ>
```

# Step 1. requirements.txt ファイルの編集

（無ければ）ファイルの末尾にでも追加してほしい。  

📄host1/requirements.txt:  

```shell
# （追加） For Tic-tac-toe
# （追加済みだろ） Django>=3.0,<4.0
# （追加済みだろ） channels>=3.0
channels_redis>=3.2
```

# Step 2. Yaml ファイルの設定（再掲）

この連載の既存の `docker-compose.yml` ファイルを用意してほしい。以下は抜粋。  

📄`host1/docker-compose.yml` （抜粋）:

```yaml
version: "3.9"

services:

  # Djangoアプリ
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    #                                   -------
    #                                   1
    # 1. Dockerコンテナ内のサーバーは localhost ではなく 0.0.0.0 と書く
    volumes:
      - .:/code
    ports:
      - "8000:8000"
```

# Step 3. Dockerfile ファイルの設定（再掲）

この連載の既存の `Dockerfile` ファイルを用意してほしい。以下は抜粋。  

📄`host1/Dockerfile` （抜粋）:

```yaml
# See also: 📖[docker docs - Quickstart: Compose and Django](https://docs.docker.com/samples/django/)

FROM python:3

# Pythonのキャッシュファイル（__pycache__ディレクトリや.pycファイル）を作成するのを止めます
ENV PYTHONDONTWRITEBYTECODE=1

# 出力をPythonでバッファリングせずにターミナルに直接送信します
ENV PYTHONUNBUFFERED=1

# コンテナに /code ディレクトリを作成し、以降、 /code ディレクトリで作業します
WORKDIR /code

# requirements.txtを /code/ ディレクトリへコピーします
ADD requirements.txt /code/

# requirements.txtに従ってpip installします
RUN pip install -r requirements.txt

# 開発環境のファイルを /code/ へコピーします
COPY . /code/
```

# Step 4. settings.py ファイルの編集

（無ければ）以下の部分を編集してほしい。  

📄host1/webapp1/settings.py:  

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # （追加） For Tic-tac-toe
    'channels',
]

# （削除） WSGI_APPLICATION = 'webapp1.wsgi.application'
# （追加）
ASGI_APPLICATION = "webapp1.asgi.application"
#                   -------
#                   1
# 1. アプリケーション フォルダー名

# （追加） See also: 📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)
CHANNEL_LAYERS = {
    'default': {
        ### Method 1: Via redis lab
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [
        #       'redis://h:<password>;@<redis Endpoint>:<port>' 
        #     ],
        # },

        ### Method 2: Via local Redis
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #      "hosts": [('127.0.0.1', 6379)],
        # },

        ### Method 3: Via In-memory channel layer
        ## Using this method.
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    },
}
```

# Step 5. コマンド実行

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

# Step 6. CSSファイルの作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/static/tic-tac-toe1/main.css`:  

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
#game_board {
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

# Step 7. CSSファイルの作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/static/tic-tac-toe1/game.js`:  

```js
// static/js/game.js

var roomCode = document.getElementById("game_board").getAttribute("room_code");
var char_choice = document.getElementById("game_board").getAttribute("char_choice");

var connectionString = 'ws://' + window.location.host + '/ws/play/' + roomCode + '/';
var gameSocket = new WebSocket(connectionString);
// Game board for maintaing the state of the game
var gameBoard = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
];
// Winning indexes.
winIndices = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
let moveCount = 0; //Number of moves done
let myturn = true; // Boolean variable to get the turn of the player.

// Add the click event listener on every block.
let elementArray = document.getElementsByClassName('square');
for (var i = 0; i < elementArray.length; i++){
    elementArray[i].addEventListener("click", event=>{
        const index = event.path[0].getAttribute('data-index');
        if(gameBoard[index] == -1){
            if(!myturn){
                alert("Wait for other to place the move")
            }
            else{
                myturn = false;
                document.getElementById("alert_move").style.display = 'none'; // Hide
                make_move(index, char_choice);
            }
        }
    })
}

// Make a move
function make_move(index, player){
    index = parseInt(index);
    let data = {
        "event": "MOVE",
        "message": {
            "index": index,
            "player": player
        }
    }

    if(gameBoard[index] == -1){
        // if the valid move, update the gameboard
        // state and send the move to the server.
        moveCount++;
        if(player == 'X')
            gameBoard[index] = 1;
        else if(player == 'O')
            gameBoard[index] = 0;
        else{
            alert("Invalid character choice");
            return false;
        }
        gameSocket.send(JSON.stringify(data))
    }
    // place the move in the game box.
    elementArray[index].innerHTML = player;
    // check for the winner
    const win = checkWinner();
    if(myturn){
        // if player winner, send the END event.
        if(win){
            data = {
                "event": "END",
                "message": `${player} is a winner. Play again?`
            }
            gameSocket.send(JSON.stringify(data))
        }
        else if(!win && moveCount == 9){
            data = {
                "event": "END",
                "message": "It's a draw. Play again?"
            }
            gameSocket.send(JSON.stringify(data))
        }
    }
}

// function to reset the game.
function reset(){
    gameBoard = [
        -1, -1, -1,
        -1, -1, -1,
        -1, -1, -1,
    ];
    moveCount = 0;
    myturn = true;
    document.getElementById("alert_move").style.display = 'inline';
    for (var i = 0; i < elementArray.length; i++){
        elementArray[i].innerHTML = "";
    }
}

// check if their is winning move
const check = (winIndex) => {
    if (
      gameBoard[winIndex[0]] !== -1 &&
      gameBoard[winIndex[0]] === gameBoard[winIndex[1]] &&
      gameBoard[winIndex[0]] === gameBoard[winIndex[2]]
    )   return true;
    return false;
};

// function to check if player is winner.
function checkWinner(){
    let win = false;
    if (moveCount >= 5) {
      winIndices.forEach((w) => {
        if (check(w)) {
          win = true;
          windex = w;
        }
      });
    }
    return win;
}

// Main function which handles the connection
// of websocket.
function connect() {
    gameSocket.onopen = function open() {
        console.log('WebSockets connection created.');
        // on websocket open, send the START event.
        gameSocket.send(JSON.stringify({
            "event": "START",
            "message": ""
        }));
    };

    gameSocket.onclose = function (e) {
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function () {
            connect();
        }, 1000);
    };
    // Sending the info about the room
    gameSocket.onmessage = function (e) {
        // On getting the message from the server
        // Do the appropriate steps on each event.
        let data = JSON.parse(e.data);
        data = data["payload"];
        let message = data['message'];
        let event = data["event"];
        switch (event) {
            case "START":
                reset();
                break;
            case "END":
                alert(message);
                reset();
                break;
            case "MOVE":
                if(message["player"] != char_choice){
                    make_move(message["index"], message["player"])
                    myturn = true;
                    document.getElementById("alert_move").style.display = 'inline';
                }
                break;
            default:
                console.log("No event")
        }
    };

    if (gameSocket.readyState == WebSocket.OPEN) {
        gameSocket.onopen();
    }
}

//call the connect function at the start.
connect();
```

# Step 8. HTMLファイルの作成

以下のファイルを作成してほしい。  

📄`host1/webapp1/templates/tic-tac-toe1/index.html`:  

```html
{% load static %} {% comment %} 👈あとで static "URL" を使うので load static します {% endcomment %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Tic Tac Toe</title>
        <link rel="stylesheet" href='{% static "/tic-tac-toe1/main.css" %}' />
    </head>
    <body>
        <div class="wrapper">
            <h1>Welcome to Tic Tac Toe Game</h1>
            <form method="POST">
                {% csrf_token %}
                <div class="form-control">
                    <label for="room">Room id</label>
                    <input id="room" type="text" name="room_code" required />
                </div>
                <div class="form-control">
                    <label for="character_choice">Your character</label>
                    <select for="character_choice" name="character_choice">
                        <option value="X">X</option>
                        <option value="O">O</option>
                    </select>
                </div>
                <input type="submit" class="button" value="Start Game" />
            </form>
        </div>

        <script src="{% static 'tic-tac-toe1/game.js' %}"></script>
        {% block javascript %} {% endblock javascript %}
    </body>
</html>
```

# Step 9. views.py ファイルを編集する

📄`host1/webapp1/views.py` に、以下の記述を追加してほしい。  

```py
from django.shortcuts import render, redirect


def indexOfTicTacToe1(request):
    """（追加） For Tic-tac-toe"""
    if request.method == "POST":
        room_code = request.POST.get("room_code")
        char_choice = request.POST.get("character_choice")
        return redirect(f'/tic-tac-toe1/{room_code}?&choice={char_choice}')
    return render(request, "tic-tac-toe1/index.html", {})
```

# Step 10. urls.py ファイルを編集する

以下の記述を追加してほしい。  

📄`host1/webapp1/urls.py` （抜粋）:

```py
from django.urls import path
from . import views

urlpatterns = [
    # ...略...

    # （追加）
    path('tic-tac-toe1/', views.indexOfTicTacToe1),
    #     -------------
    #     1
    # 1. URLの一部
]
```

# Step 11. Web画面へアクセス

（していなければ）Dockerコンテナの起動  

```shell
cd host1

docker-compose up
```

📖 [http://localhost:8000/tic-tac-toe1/](http://localhost:8000/tic-tac-toe1/)  
