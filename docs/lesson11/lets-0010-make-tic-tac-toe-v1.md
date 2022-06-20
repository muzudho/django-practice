# 目的

Webサーバーと、クライアント側のアプリ間で通信する練習をしたい。  
だから 〇×ゲーム（Tic tac toe）のサンプルプログラムを真似する。  
１人２役で２窓で遊ぶ  

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
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1
        │   │       └── 📂practice
        │   │           └── 📄vuetify-desserts.json
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂<いろいろ>-practice
        │   │           └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂websock_practice1
        │   │       └── 📂v1
        │   │           └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄routing1.py
        │   └── 📄urls.py
        ├── 📄asgi.py
        ├── 📄.env
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        ├── 📄settings.py
        └── 📄urls.py
```

以下、参考にした元記事は 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/) だ。  
わたしの記事は単に **やってみた** ぐらいの位置づけだ。  

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. プログラミング環境更新 - requirements.txt ファイル

（無ければ）ファイルの末尾にでも追加してほしい  

```plaintext
    └── 📂host1
👉      └── 📄requirements.txt
```

```shell
channels_redis>=3.2
```

# Step 3. コマンド実行

以下のコマンドを打鍵してほしい  

```shell
# settings.py を編集したのでマイグレーションし直します
docker-compose run --rm web python3 manage.py migrate
#                       ---
#                       1
# 1. docker-compose.yml ファイルに書いてある services の子要素名
```

# Step 4. Web ページのスタイル作成 - main.css ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1                         # 新規作成。複数のアプリケーションを入れるフォルダー。末尾の 1 は文字列検索しやすいように付けているだけで特別な意味はない
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       └── 📂static
        │           └── 📂tic_tac_toe       # アプリケーション フォルダーと同名。フォルダー構成が冗長になるが、HTMLソースが読みやすくなるという工夫
        │               └── 📂v1o1          # version 1.1 ぐらいの意味。小数を使うと刻みやすい。 1.0 ではなく 1.1 から始めると、1.0.1 を挿入できるメリットがある
👉      │                   └── 📄main.css
        └── 📄requirements.txt
```

```css
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

# Step 5. 機能作成 - play.js ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       └── 📂static
        │           └── 📂tic_tac_toe       # アプリケーション フォルダーと同名
        │               └── 📂v1o1
        │                   ├── 📄main.css
👉      │                   └── 📄play.js
        └── 📄requirements.txt
```

```js
// See also: 📖[Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)

var roomName = document.getElementById("board").getAttribute("room_name");
var myPiece = document.getElementById("board").getAttribute("my_piece");

var connectionString = `ws://${window.location.host}/tic-tac-toe/v1o1/playing/${roomName}/`;
//                      ----]----------------------- -------------------------------------
//                      1    2                       3
//                      ------------------------------------------------------------------
//                      4
// 1. スキーム : Web Socket
// 2. ホスト アドレス
// 3. パス
// 4. URL

var webSock1 = new WebSocket(connectionString);

const PC_EMPTY = -1; // A square without piece; PC is piece
// Game board for maintaing the state of the game
var board = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];

// SQ is square
// +---------+
// | 0  1  2 |
// | 3  4  5 |
// | 6  7  8 |
// +---------+
const SQ_0 = 0;
const SQ_1 = 1;
const SQ_2 = 2;
const SQ_3 = 3;
const SQ_4 = 4;
const SQ_5 = 5;
const SQ_6 = 6;
const SQ_7 = 7;
const SQ_8 = 8;

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
    [SQ_2, SQ_4, SQ_6],
];
let countOfMove = 0; // Number of moves done
let myTurn = true; // Boolean variable to get the turn of the player.

// Add the click event listener on every block.
let elementArrayOfSquare = document.getElementsByClassName("square");
for (const element of elementArrayOfSquare) {
    element.addEventListener("click", (event) => {
        const sq = event.path[0].getAttribute("square"); // Square; 0 <= sq
        if (board[sq] == PC_EMPTY) {
            if (!myTurn) {
                alert("Wait for other to place the move");
            } else {
                myTurn = false;
                document.getElementById("alert_move").style.display = "none"; // Hide
                makeMove(sq, myPiece);
            }
        }
    });
}

/**
 * Make a move
 * @param {*} sq - Square; 0 <= sq
 * @param {*} myPiece
 * @returns
 */
function makeMove(sq, myPiece) {
    sq = parseInt(sq);
    let data = {
        event: "MOVE",
        message: {
            index: sq,
            player: myPiece,
        },
    };

    if (board[sq] == PC_EMPTY) {
        // if the valid move, update the board
        // state and send the move to the server.
        countOfMove++;

        switch (myPiece) {
            case "X":
                board[sq] = 1;
                break;
            case "O":
                board[sq] = 0;
                break;
            default:
                alert(`Invalid my piece = ${myPiece}`);
                return false;
        }

        webSock1.send(JSON.stringify(data));
    }
    // place the move in the game box.
    elementArrayOfSquare[sq].innerHTML = myPiece;
    // check for the winner
    const gameOver = isGameOver();
    if (myTurn) {
        // if player winner, send the END event.
        if (gameOver) {
            data = {
                event: "END",
                message: `${myPiece} is a winner. Play again?`,
            };
            webSock1.send(JSON.stringify(data));
        } else if (!gameOver && countOfMove == 9) {
            data = {
                event: "END",
                message: "It's a draw. Play again?",
            };
            webSock1.send(JSON.stringify(data));
        }
    }
}

// function to reset the game.
function reset() {
    board = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY];
    countOfMove = 0;
    myTurn = true;
    document.getElementById("alert_move").style.display = "inline";
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
    return board[squaresOfWinPattern[0]] !== PC_EMPTY && board[squaresOfWinPattern[0]] === board[squaresOfWinPattern[1]] && board[squaresOfWinPattern[0]] === board[squaresOfWinPattern[2]];
}

/**
 * function to check if player is winner.
 * @returns I won
 */
function isGameOver() {
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
        console.log("WebSockets connection created.");
        webSock1.send(
            JSON.stringify({
                event: "START",
                message: "",
            })
        );
    };

    webSock1.onclose = (e) => {
        console.log("Socket is closed. Reconnect will be attempted in 1 second.", e.reason);
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
        let message = data["message"];
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
                if (message["player"] != myPiece) {
                    makeMove(message["index"], message["player"]);
                    myTurn = true;
                    document.getElementById("alert_move").style.display = "inline";
                }
                break;
            default: // ちゃんと動いているようなら消す
                console.log(`[Message] (Others) e=${e.data}`);
                console.log("No event");
        }
    };

    if (webSock1.readyState == WebSocket.OPEN) {
        console.log("Open socket.");
        webSock1.onopen();
    }
}

//call the connect function at the start.
connect();
```

# Step 6. 対局申込画面作成 - match_application.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       └── 📂templates
        │           └── 📂tic_tac_toe       # アプリケーション フォルダーと同名
        │               └── 📂v1o1
👉      │                   └── 📄match_application.html
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
        <link rel="stylesheet" href='{% static "tic_tac_toe/v1o1/main.css" %}' />
        <!--                                    =========================
                                                1
        1. `host1/apps1/tic_tac_toe/static/tic_tac_toe/v1o1/main.css`
                                           =========================
        -->
    </head>
    <body>
        <div class="wrapper">
            <h1>Welcome to Tic Tac Toe Game Copy</h1>

            <p>📖 Original: <a href="https://blog.logrocket.com/django-channels-and-websockets/">Django Channels and WebSockets</a></p>

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

# Step 7. 対局画面作成 - playing.html ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       └── 📂templates
        │           └── 📂tic_tac_toe       # アプリケーション フォルダーと同名
        │               └── 📂v1o1
        │                   ├── 📄match_application.html
👉      │                   └── 📄playing.html
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
        <link rel="stylesheet" href='{% static "tic_tac_toe/v1o1/main.css" %}' />
        <!--                                    =========================
                                                1
        1. `host1/apps1/tic_tac_toe/static/tic_tac_toe/v1o1/main.css`
                                           =========================
        -->
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

        <script src="{% static 'tic_tac_toe/v1o1/play.js' %}"></script>
        <!--                    ========================
                                1
        1. `host1/apps1/tic_tac_toe/static/tic_tac_toe/v1o1/play.js`
                                           ========================
        -->
        {% block javascript %} {% endblock javascript %}
    </body>
</html>
```

# Step 8. ビュー作成 - resources.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe       # アプリケーション フォルダーと同名
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       └── 📂views
        │           └── 📂v1o1              # HTMLレンダリングで参照されるパスではないから、アプリケーション フォルダーと同名のフォルダーは要らない
👉      │               └── 📄resources.py
        └── 📄requirements.txt
```

```py
"""〇×ゲームの練習１．１"""
from django.http import Http404
from django.shortcuts import render, redirect


# 以下、リソース


class MatchApplication():
    """対局申込"""

    _path_of_http_playing = "/tic-tac-toe/v1o1/playing/{0}/?&mypiece={1}"
    #                                      ^^^ one o one
    #                        -------------------------------------------
    #                        1
    # 1. http://example.com:8000/tic-tac-toe/v1o1/playing/Elephant/?&mypiece=X
    #                           ----------------------------------------------

    _path_of_html = "tic_tac_toe/v1o1/match_application.html"
    #                             ^^^ one o one
    #                ---------------------------------------
    #                1
    # 1. host1/apps1/tic_tac_toe/templates/tic_tac_toe/v1o1/match_application.html
    #                                      ---------------------------------------

    def render(request):
        """描画"""
        return render_match_application(request, MatchApplication._path_of_http_playing, MatchApplication._path_of_html)


class Playing():
    """対局"""

    _path_of_html = "tic_tac_toe/v1o1/playing.html"
    #                             ^^^ one o one
    #                -----------------------------
    #                                            1
    # 1. host1/apps1/tic_tac_toe/templates/tic_tac_toe/v1o1/playing.html
    #                                      -----------------------------

    def render(request, room_name):
        """描画"""
        return render_playing(request, room_name, Playing._path_of_html)


# 以下、関数


def render_match_application(request, path_of_http_playing, path_of_html):
    """対局申込 - 描画"""

    if request.method == "POST":
        # 送信後
        room_name = request.POST.get("room_name")
        myPiece = request.POST.get("my_piece")
        # TODO バリデーションチェックしたい
        return redirect(path_of_http_playing.format(room_name, myPiece))

    # 訪問後
    return render(request, path_of_html, {})


def render_playing(request, room_name, path_of_html):
    """対局 - 描画"""

    myPiece = request.GET.get("mypiece")
    if myPiece not in ['X', 'O']:
        raise Http404(f"My piece '{myPiece}' does not exists")

    context = {
        "my_piece": myPiece,
        "room_name": room_name
    }
    return render(request, path_of_html, context)
```

# Step 9. ルート新規作成 - apps1/tic_tac_toe/urls.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
👉      │       └── 📄urls.py                   # こちら
        ├── 📄requirements.txt
❌      └── 📄urls.py                           # これではない
```

```py
from django.urls import path

# 〇×ゲームの練習１
from apps1.tic_tac_toe.views.v1o1 import resources as tic_tac_toe_v1
#    ----- ----------- ----------        ---------    --------------
#    1     2           3                 4            5
#    ----------------------------
#    6
# 1. 開発者用ディレクトリーの一部
# 2. アプリケーション フォルダー名
# 3. ディレクトリー名
# 4. Python ファイル名。拡張子抜き
# 5. `4.` の別名
# 6. モジュール名


urlpatterns = [

    # +----
    # | 〇×ゲーム１

    # 対局申込
    path('tic-tac-toe/v1o1/match-application/',
         # ----------------------------------
         # 1
         tic_tac_toe_v1.MatchApplication.render),
    #    --------------------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v1o1/match-application/` のような URL のパスの部分
    #                              -----------------------------------
    # 2. tic_tac_toe_v1 (別名)ファイルの MatchApplication クラスの render 静的メソッド

    # 対局中
    path('tic-tac-toe/v1o1/playing/<str:room_name>/',
         # ----------------------------------------
         # 1
         tic_tac_toe_v1.Playing.render),
    #    -----------------------------
    #    2
    # 1. 例えば `http://example.com/tic-tac-toe/v1o1/playing/<部屋名>/` のような URL のパスの部分。
    #                              ----------------------------------
    #    <部屋名> に入った文字列は room_name 変数に渡されます
    # 2. tic_tac_toe_v1 (別名)ファイルの Playing クラスの render 静的メソッド

    # | 〇×ゲーム１
    # +----
]
```

# Step 10. 総合ルート編集 - host1/urls.py ファイル

以下の既存のファイルに、以下のソースをマージしてほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
❌      │       └── 📄urls.py                   # これではない
        ├── 📄requirements.txt
👉      └── 📄urls.py                           # こちら
```

```py
from django.urls import include, path


# ...中略...


urlpatterns = [


    # ...中略...


    # +----
    # | 〇×ゲーム アプリケーション

    # ぶら下げ
    path('', include('apps1.tic_tac_toe.urls')),
    #    --           ----------------------
    #    1            2
    # 1. 例えば `http://example.com/` のような URLの直下
    # 2. `host1/apps1/tic_tac_toe.urls.py` の urlpatterns を (1.) にぶら下げます
    #           ----------------------

    # | 〇×ゲーム アプリケーション
    # +----
]
```

# Step 11. consumer.py ファイルの作成

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂websocks
        │       │   └── 📂v1o1                  # HTMLレンダリングで参照されるパスではないから、アプリケーション フォルダーと同名のフォルダーは要らない
👉      │       │       └── 📄consumer.py
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
        │       └── 📄urls.py
        ├── 📄requirements.txt
        └── 📄urls.py
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
                'type': 'send_message',  # type属性は必須
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',  # type属性は必須
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',  # type属性は必須
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

# Step 12. Webソケット用ルート新規作成 - urls_ws1.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂websocks
        │       │   └── 📂v1o1
        │       │       └── 📄consumer.py
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
👉      │       ├── 📄urls_ws1.py               # 末尾の 1 は文字列検索しやすいように付けているだけで特別な意味はない
        │       └── 📄urls.py
        ├── 📄requirements.txt
        └── 📄urls.py
```

```py
# See also: 📖 [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url

# 〇×ゲームの練習１
from apps1.tic_tac_toe.websocks.v1o1.consumer import TicTacToeV1Consumer
#    ----- ----------- ------------- --------        -------------------
#    1     2           3             4               5
#    ----------------------------------------
#    6
# 1. 開発者用ディレクトリーの一部
# 2. アプリケーション フォルダー名
# 3. ディレクトリー名
# 4. Python ファイル名。拡張子抜き
# 5. クラス名
# 6. モジュール名

websocket_urlpatterns = [
    # 〇×ゲームの練習１
    url(r'^tic-tac-toe/v1o1/playing/(?P<room_name>\w+)/$',
        # ----------------------------------------------
        # 1
        TicTacToeV1Consumer.as_asgi()),
    #   -----------------------------
    #   2
    # 1. 例えば `http://example.com/tic-tac-toe/v1o1/playing/Elephant/` のようなURLのパスの部分の、Django での正規表現の書き方。
    #    room_name は変数として渡される
    # 2. クラス名とメソッド。 URL を ASGI形式にする
]
```

# Step 13. ASGI設定 - asgi.py ファイル

以下の既存のファイルを編集してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂websocks
        │       │   └── 📂v1o1
        │       │       └── 📄consumer.py
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
        │       ├── 📄urls_ws1.py
        │       └── 📄urls.py
👉      ├── 📄asgi.py
        ├── 📄requirements.txt
        └── 📄urls.py
```

```py
import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import apps1.tic_tac_toe.urls_ws1
#      ----------------- --------
#      1                 2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

import webapp1.routing1
#      ------- --------
#      1       2
# 1. アプリケーション フォルダー名
# 2. Pythonファイル名（拡張子除く）

# 複数のアプリケーションの websocket_urlpatterns をマージします
websocket_urlpatterns_merged = []
websocket_urlpatterns_merged.extend(
    apps1.tic_tac_toe.urls_ws1.websocket_urlpatterns)
websocket_urlpatterns_merged.extend(webapp1.routing1.websocket_urlpatterns)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
#                                                --------
#                                                1
# 1. 設定モジュール名 `host1/settings.py`
#                          --------
#    例えばレッスンの最初に webapp1 アプリケーションを作成した場合、
#    デフォルトでは webapp1 アプリケーション用の設定モジュール名 `webapp1.settings` を指定するようになっているので、
#                                                            ------- --------
#                                                            1o1     1o2
#    1o1. アプリケーション フォルダー名
#    1o2. settings.py ファイルの拡張子抜き
#
#    複数のアプリケーションの設定ファイルを指定するよう、トップフォルダーの settings.py に変更する

# （削除） django.setup()

# （削除） application = get_asgi_application()

application = ProtocolTypeRouter({
    # （削除） "http": AsgiHandler(),
    "http": get_asgi_application(),  # 追加
    "websocket": AuthMiddlewareStack(  # 追加
        URLRouter(
            # * 削除
            # webapp1.routing1.websocket_urlpatterns
            # * 追加
            websocket_urlpatterns_merged
        )
    ),
})
```

# Step 14. Djangoの設定 - settings.py ファイル

以下の既存のファイルを編集してほしい  

```plaintext
    └── 📂host1
        ├── 📂apps1
        │   └── 📂tic_tac_toe               # アプリケーション フォルダー
        │       ├── 📂static
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄main.css
        │       │           └── 📄play.js
        │       ├── 📂templates
        │       │   └── 📂tic_tac_toe
        │       │       └── 📂v1o1
        │       │           ├── 📄match_application.html
        │       │           └── 📄playing.html
        │       ├── 📂websocks
        │       │   └── 📂v1o1
        │       │       └── 📄consumer.py
        │       ├── 📂views
        │       │   └── 📂v1o1
        │       │       └── 📄resources.py
        │       ├── 📄urls_ws1.py
        │       └── 📄urls.py
        ├── 📄asgi.py
        ├── 📄requirements.txt
👉      ├── 📄settings.py
        └── 📄urls.py
```

```py
# ...略...


# Application definition

INSTALLED_APPS = [
    # あなたが追加したアプリケーション
    'apps1.tic_tac_toe',                # 追加
    'webapp1',

    # Djangoの標準アプリケーション
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # ...略...


]


# ...略...


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # 'DIRS' 配列には全く指定しないか、１つでも指定するなら デフォルトのテンプレート フォルダーを含めるようにしてください


            # ...略...


            # * 以下を追加
            #
            # +----
            # | 〇×ゲーム アプリケーション

            os.path.join(BASE_DIR, 'apps1', 'tic_tac_toe', 'templates'),
            #            --------   -----    -----------    ---------
            #            1          2        3              4
            #
            # Example: /host1/apps1/tic_tac_toe/templates/tic_tac_toe/v1o1/match_application.html
            #          ------ ----- ----------- ---------
            #          1      2     3           4
            #
            # 1. あなたの開発用ディレクトリー（例えば host1）が code に差し替わっています
            # 2. 開発用ディレクトリー
            # 3. アプリケーション フォルダー
            # 4. テンプレート フォルダー

            # | 〇×ゲーム アプリケーション
            # +----
        ],
        'APP_DIRS': True,
        'OPTIONS': {


            # ...略...


        },
    },
]

```

# Step 15. Web画面へアクセス

このゲームは２人用なので、Webページを２窓で開き、片方が X プレイヤー、もう片方が O プレイヤーとして遊んでください  

📖 [http://localhost:8000/tic-tac-toe/v1o1/match-application/](http://localhost:8000/tic-tac-toe/v1o1/match-application/)  

# 次の記事

📖 [DockerでTic-Tac-Toeの思考エンジンを作ろう！](https://qiita.com/muzudho1/items/69021deb9ec541406cfb)  

# 参考にした記事

## Web Socket

📖 [Django Channels and WebSockets](https://blog.logrocket.com/django-channels-and-websockets/)  

## Django settings

📖 [スタティックファイルの利用](https://python.keicode.com/django/how-to-serve-static-files.php)  
