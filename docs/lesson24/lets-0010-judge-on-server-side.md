# 目的

サーバーサイドで勝敗判定したい

# はじめに

この記事は Lesson01 から順に全部やってこないと ソースが足りず実行できないので注意されたい。  
連載の目次: 📖 [DjangoとDockerでゲーム対局サーバーを作ろう！](https://qiita.com/muzudho1/items/eb0df0ea604e1fd9cdae)  

この記事のアーキテクチャ:  

| Key       | Value                                     |
| --------- | ----------------------------------------- |
| OS        | Windows10                                 |
| Container | Docker                                    |
| Editor    | Visual Studio Code （以下 VSCode と表記） |

ディレクトリ構成を抜粋すると 以下のようになっている。  

```plaintext
    ├── 📂host_local1
    │    └── 📄<いろいろ>
    └── 📂host1
        ├── 📂data
        │   └── 📂db
        │       └── （たくさんのもの）
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂models
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂models_helper
        │   │   └── 📄<いろいろ>.py
        │   ├── 📂static
        │   │   ├── 📂allauth-customized
        │   │   ├── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │   │   └── 📂practice
        │   │   │       └── 📄<いろいろ>.js
        │   │   └── 🚀favicon.ico
        │   ├── 📂templates
        │   │   ├── 📂allauth-customized
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂tic-tac-toe
        │   │           ├── 📂v1
        │   │           └── 📂v2
        │   │               └── 📄<いろいろ>.html
        │   ├── 📂views
        │   │   └── 📂practice
        │   │       └── 📄<いろいろ>.py
        │   ├── 📂websocks
        │   │   └── 📂tic_tac_toe
        │   │       ├── 📂v1
        │   │       └── 📂v2
        │   │           └── 📄<いろいろ>.py
        │   ├── 📄admin.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   └── 📄urls.py
        ├── 📄.env
        ├── 📄asgi.py
        ├── 🐳docker-compose.yml
        ├── 🐳Dockerfile
        ├── 📄manage.py
        ├── 📄requirements.txt
        └── 📄<いろいろ>
```

# Step 1. Dockerコンテナの起動

（していなければ） Docker コンテナを起動しておいてほしい  

```shell
# docker-compose.yml ファイルを置いてあるディレクトリーへ移動してほしい
cd host1

# Docker コンテナ起動
docker-compose up
```

# Step 2. 物定義 - things.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      └── 📄things.py
```

```py
# +--------
# | 駒
# |

# PC は Piece （駒）の略です。
PC_EMPTY = 0
"""Pieceがないことを表します"""

PC_X = 1
"""先手"""

PC_O = 2
"""後手"""

# ラベル
PC_EMPTY_LABEL = ""
"""空きマス"""

PC_X_LABEL = "X"
"""先手"""

PC_O_LABEL = "O"
"""後手"""

# |
# | 駒
# +--------

# +--------
# | 盤
# |

BOARD_AREA = 9
"""盤上の升の数"""

SQ_0 = 0
"""SQ is square
+---------+
| 0  1  2 |
| 3  4  5 |
| 6  7  8 |
+---------+
"""

SQ_1 = 1
"""1のマス"""

SQ_2 = 2
"""2のマス"""

SQ_3 = 3
"""3のマス"""

SQ_4 = 4
"""4のマス"""

SQ_5 = 5
"""5のマス"""

SQ_6 = 6
"""6のマス"""

SQ_7 = 7
"""7のマス"""

SQ_8 = 8
"""8のマス"""


class Board ():
    def __init__(self):
        """"""

        self._squares = [PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY,
                         PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY, PC_EMPTY]
        """各マス"""

    def getPieceBySq(self, sq):
        """盤上のマス番号で示して、駒を取得

        Parameters
        ----------
        sq : int
            マス番号

        Returns
        -------
        _type_
            _description_
        """
        return self._squares[sq]

    def setPiece(self, sq, piece):
        """盤上のマスに駒を上書きします

        Parameters
        ----------
        sq : int
            マス番号
        piece : str
            駒
        """
        self._squares[sq] = piece

    def dump(self, indent):
        """ダンプ"""
        return f"""
{indent}Board
{indent}-----
{indent}_squares: {self._squares}"""


# | 盤
# |
# +--------

# +--------
# | 棋譜
# |


class Record ():
    def __init__(self):
        self._squares = []

    def push(self, sq):
        """追加

        Parameters
        ----------
        sq : int
            駒を置いた場所
        """
        self._squares.append(sq)

    def pop(self):
        self._squares.pop()

    @property
    def length(self):
        return len(self._squares)

    def dump(self, indent):
        """ダンプ"""
        return f"""
{indent}Record
{indent}------
{indent}_squares: ${self._squares}"""


# | 棋譜
# |
# +--------
```

# Step 3. 概念定義 - concepts.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      ├── 📄concepts.py
                        └── 📄things.py
```

```py
from webapp1.views.tic_tac_toe.v3o2 import things
#    ------- ----------------------        ------
#    1       2                             3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class RoomState ():
    """部屋の状態"""

    @staticmethod
    @property
    def none():
        """ゲームしてません"""
        return 0

    @staticmethod
    @property
    def playing():
        """ゲーム中"""
        return 1

    def __init__(self, value, onChangeValue):
        """生成

        Parameters
        ----------
        value : int
            _description_
        onChangeValue : function
            値の変更時
        """
        print(f"[RoomState constructor]")

        self._value = value
        self._onChangeValue = onChangeValue

    @property
    def value(self):
        """値"""
        return self._value

    @value.setter
    def value(self, value):
        print(f"[RoomState set value]")

        if self._value == value:
            return

        oldValue = self._value
        self._value = value
        self._onChangeValue(oldValue, self._value)

    def dump(self, indent):
        """ダンプ

        Parameters
        ----------
        indent : str
            インデント
        """
        return f"""
{indent}RoomState
{indent}---------
{indent}_value: {self._value}"""


class MyTurn ():
    """自分のターン"""

    def __init__(self, myPiece):
        """生成

        Parameters
        ----------
        myPiece : str
            自分の駒。 "X", "O", "_"
        """

        self._isMe = myPiece == things.PC_X_LABEL
        """自分の手番か（初回は先手）"""

    @property
    def isTrue(self):
        """真実か？"""
        return self._isMe

    @property.isTrue
    def isTrue(self, value):
        self._isMe = value
        # vue1.raiseMyTurnChanged()

    def dump(self, indent):
        """ダンプ

        Parameters
        ----------
        indent : str
            インデント

        Returns
        -------
        str
            ダンプ
        """
        return f"""
{indent}MyTurn
{indent}------
{indent}_isMe: ${self._isMe}"""


class GameoverSet():
    """ゲームオーバー集合

    * 自分視点
    """

    @ staticmethod
    @ property
    def none():
        """ゲームオーバーしてません"""
        return 0

    @ staticmethod
    @ property
    def win():
        """勝ち"""
        return 1

    @ staticmethod
    @ property
    def draw():
        """引き分け"""
        return 2

    @ staticmethod
    @ property
    def lose():
        """負け"""
        return 3

    def __init__(self, value):
        """生成

        Parameters
        ----------
        value : int
            値
        """
        self._value = value

    @property
    def value(self):
        """値"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def dump(self, indent):
        """ダンプ

        Parameters
        ----------
        indent : str
            インデント
        """
        if self._value == GameoverSet.none:
            text = "none"
        elif self._value == GameoverSet.win:
            text = "win"
        elif self._value == GameoverSet.draw:
            text = "draw"
        elif self._value == GameoverSet.lose:
            text = "lose"
        else:
            raise ValueError(
                f"[GameoverSet dump] Unexpected value={self._value}")

        return f"""
{indent}GameoverSet
{indent}-----------
{indent}_value: {text}"""


WIN_PATTERN = [
    [things.SQ_0, things.SQ_1, things.SQ_2],
    """
    +---------+
    | *  *  * |
    | .  .  . |
    | .  .  . |
    +---------+
    """

    [things.SQ_3, things.SQ_4, things.SQ_5],
    """
    +---------+
    | .  .  . |
    | *  *  * |
    | .  .  . |
    +---------+
    """

    [things.SQ_6, things.SQ_7, things.SQ_8],
    """
    +---------+
    | .  .  . |
    | .  .  . |
    | *  *  * |
    +---------+
    """

    [things.SQ_0, things.SQ_3, things.SQ_6],
    """
    +---------+
    | *  .  . |
    | *  .  . |
    | *  .  . |
    +---------+
    """

    [things.SQ_1, things.SQ_4, things.SQ_7],
    """
    +---------+
    | .  *  . |
    | .  *  . |
    | .  *  . |
    +---------+
    """

    [things.SQ_2, things.SQ_5, things.SQ_8],
    """
    +---------+
    | .  .  * |
    | .  .  * |
    | .  .  * |
    +---------+
    """

    [things.SQ_0, things.SQ_4, things.SQ_8],
    """
    +---------+
    | *  .  . |
    | .  *  . |
    | .  .  * |
    +---------+
    """

    [things.SQ_2, things.SQ_4, things.SQ_6],
    """
    +---------+
    | .  .  * |
    | .  *  . |
    | *  .  . |
    +---------+
    """
]
"""駒が３つ並んでいるパターン"""


def flipTurn(piece):
    """手番反転

    Returns
    -------
    str
        piece
    """

    if piece == things.PC_X_LABEL:
        return things.PC_O_LABEL
    elif piece == things.PC_O_LABEL:
        return things.PC_X_LABEL

    return piece
```

# Step 4. 局面定義 - positions.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄concepts.py
👉                      ├── 📄positions.py
                        └── 📄things.py
```

```py
from webapp1.views.tic_tac_toe.v3o2.things import Board, Record
#    ------- ---------------------- ------        -------------
#    1       2                      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名

from webapp1.views.tic_tac_toe.v3o2.concepts import MyTurn
#    ------- ---------------------- --------        ------
#    1       2                      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. クラス名


class Position():
    """局面"""

    def __init__(self, myPiece):
        """初期化

        * 対局開始時

        Parameters
        ----------
        myPiece : str
            "X", "O", "_"
        """
        print(f"[Position constructor] myPiece=${myPiece}")

        self._board = Board()
        """盤面"""

        self._record = Record()
        """棋譜"""

        self._myTurn = MyTurn(myPiece)
        """自分の手番"""

    @property
    def board(self):
        """盤"""
        return self._board

    @property
    def record(self):
        """棋譜"""
        return self._record

    @property
    def myTurn(self):
        """自分のターン"""
        return self._myTurn

    @property
    def isBoardFill(self):
        """マスがすべて埋まっていますか"""
        return self.record.length == 9

    @property
    def isThere3SamePieces(self):
        """同じ駒が３個ありますか"""
        return 5 <= self.record.length

    def dump(self, indent):
        """ダンプ"""
        return f"""
{indent}Position
{indent}--------
{indent}{self._board.dump(indent + "    ")}
{indent}{self._record.dump(indent + "    ")}
{indent}{self._myTurn.dump(indent + "    ")}"""
```

# Step 5. ユーザー操作定義 - user_ctrl.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄concepts.py
                        ├── 📄positions.py
                        ├── 📄things.py
👉                      └── 📄user_ctrl.py
```

```py
from webapp1.views.tic_tac_toe.v3o2.things import PC_EMPTY, PC_X_LABEL, PC_O_LABEL, PC_X, PC_O
#    ------- ---------------------- ------        --------...
#    1       2                      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 変数，クラス名等


class UserCtrl ():
    """ユーザーコントロール"""

    def __init__(self):
        """生成"""

        def doNothing():
            pass

        self._onDoMove = doNothing
        """イベントリスナー"""

    @property
    def onDoMove(self):
        return self._onDoMove

    @onDoMove.setter
    def onDoMove(self, value):
        """駒を置いたとき"""
        self._onDoMove = value

    def doMove(self, position, piece, sq):
        """駒を置きます

        Parameters
        ----------
        position : Position
            局面
        piece : str
            X か O
        sq : int
            升番号 0 <= sq

        Returns
        -------
        _type_
            駒を置けたら真、それ以外は偽
        """

        if position.getPieceBySq(sq) == PC_EMPTY:
            # 空升なら

            self._playeq.incrementCountOfMove()
            # 手数を１増やします

            # 駒を置きます
            if piece == PC_X_LABEL:
                self._playeq.setPiece(sq, PC_X)
            elif piece == PC_O_LABEL:
                self._playeq.setPiece(sq, PC_O)
            else:
                print(f"[Error] Invalid piece={piece}")
                return False

            print(f"[UserCtrl doMove] sq={sq} piece={piece}")
            self._onDoMove(sq, piece)

        return True
```

# Step 6. 審判操作定義 - judge_ctrl.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄concepts.py
👉                      ├── 📄judge_ctrl.py
                        ├── 📄positions.py
                        ├── 📄things.py
                        └── 📄user_ctrl.py
```

```py
from webapp1.views.tic_tac_toe.v3o2.things import PC_EMPTY
#    ------- ---------------------- ------        --------
#    1       2                      3             4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 変数，クラス名等

from webapp1.views.tic_tac_toe.v3o2.concepts import WIN_PATTERN, GameoverSet
#    ------- ---------------------- --------        -----------...
#    1       2                      3               4
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き
# 4. 変数，クラス名等


class JudgeCtrl():
    """審判コントロール"""

    def __init__(self):
        """生成"""

        def ignore(piece_moved, gameover_set_value):
            pass

        self._onJudged = ignore
        """判断したとき"""

    @property
    def onJudged(self, value):
        """判断したとき"""
        self._onJudged = value

    def doJudge(self, position, piece_moved):
        """ゲームオーバー判定

        * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください

        Parameters
        ----------
        position : Position
            局面"""

        gameover_set_value = self.makeGameoverState(position)
        print(f"[doJudge] gameover_set_value={gameover_set_value}")
        self._onJudged(piece_moved, gameover_set_value)

    def makeGameoverState(self, position):
        """ゲームオーバー判定

        * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください

        Returns
        -------
        ゲームオーバー状態
        """
        if self._playeq.isThere3SamePieces():
            for squaresOfWinPattern in WIN_PATTERN:
                if self.isPieceInLine(position, squaresOfWinPattern):
                    if position.turn.isMe:
                        # 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return GameoverSet.lose
                    else:
                        # 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return GameoverSet.win

        if position.isBoardFill:
            # 勝ち負けが付かず、盤が埋まったら引き分け
            return GameoverSet.draw

        # ゲームオーバーしてません
        return GameoverSet.none

    def isPieceInLine(self, position, squaresOfWinPattern):
        """駒が３つ並んでいるか？

        Parameters
        ----------
        position : Position
            局面
        squaresOfWinPattern : _type_
            勝ちパターン

        Returns
        -------
        _type_
            並んでいれば真、それ以外は偽
        """
        return position.board.getPieceBySq(squaresOfWinPattern[0]) != PC_EMPTY and \
            position.board.getPieceBySq(squaresOfWinPattern[0]) == position.board.getPieceBySq(squaresOfWinPattern[1]) and \
            position.board.getPieceBySq(
                squaresOfWinPattern[0]) == position.board.getPieceBySq(squaresOfWinPattern[2])
```

# Step 7. エンジン作成 - building.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄concepts.py
👉                      ├── 📄building.py
                        ├── 📄judge_ctrl.py
                        ├── 📄positions.py
                        ├── 📄things.py
                        └── 📄user_ctrl.py
```

```py
from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class Engine():
    """ゲームエンジン"""

    def __init__(self, setMessageFromServer, reconnect, roomName, myPiece, convertPartsToConnectionString):
        """生成

        Parameters
        ----------
        setMessageFromServer : _type_
            サーバーからのメッセージをセットする関数
        reconnect : _type_
            再接続ラムダ関数
        roomName : _type_
            部屋名
        myPiece : _type_
            X か O
        convertPartsToConnectionString : function
            接続文字列を返す関数(roomName, myPiece) = >{return connectionString
        """

        self._setMessageFromServer = setMessageFromServer
        self._reconnect = reconnect

        self._myPiece = myPiece
        """自分の駒"""

        self._winner = ""
        """あれば勝者 "X", "O" なければ空文字列"""

        self._connection = Connection()
        """接続"""
        self._connection.setup(
            roomName, myPiece, convertPartsToConnectionString)

        self._messageSender = MessageSender()
        """メッセージ一覧"""

        self._position = Position()
        """局面"""

        self._userCtrl = UserCtrl(self._position)
        """ユーザーコントロール"""

        self._judgeCtrl = JudgeCtrl(self._position, self._userCtrl)
        """審判コントロール"""

        def onWon():
            response = self.messageSender.createWon(myPiece)
            # self._connection.webSock1.send(JSON.stringify(response))

        self._judgeCtrl.onWon = onWon
        """どちらかが勝ったとき"""

        def onDraw():
            response = self.messageSender.createDraw()
            # self._connection.webSock1.send(JSON.stringify(response))

        self._judgeCtrl.onDraw = onDraw
        """引き分けたとき"""

        self.connect()

    def setup(self, setLabelOfButton):
        def onDoMove(sq, piece):
            # ボタンのラベルを更新
            setLabelOfButton(sq, piece)

            print(f"[onDoMove] self._myPiece={self._myPiece} piece={piece}")

            # 自分の指し手なら送信
            if self._myPiece == piece:
                response = self.messageSender.createDoMove(sq, piece)
                # self._connection.webSock1.send(JSON.stringify(response))

        self._userCtrl.onDoMove = onDoMove
        """１手進めたとき"""

    @property
    def connection(self):
        """接続"""
        return self._connection

    @property
    def messageSender(self):
        """メッセージ一覧"""
        return self._messageSender

    @property
    def playeq(self):
        """局面"""
        return self._position

    @property
    def userCtrl(self):
        """ユーザーコントロール"""
        return self._userCtrl

    @property
    def judgeCtrl(self):
        """審判コントロール"""
        return self._judgeCtrl

    @property
    def winner(self):
        """勝者"""
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    def getGameoverSet(self):
        """対局結果

        勝者 "X", "O" を、勝敗 WIN, DRAW, LOSE, NONE に変換
        """

        if self._winner == game_rule.PC_EMPTY_LABEL:
            return GameoverSet.draw
        elif self._winner == vue1.building.connection.myPiece:
            return GameoverSet.win
        elif self._winner == self.flipTurn(vue1.building.connection.myPiece):
            return GameoverSet.lose

        return GameoverSet.none

    def connect(self):
        """接続"""
        pass
        '''
        self._connection.connect(
            # Webソケットを開かれたとき
            ()=> {
                console.log("WebSockets connection created.")
                let response=this.messageSender.createStart()
                this._connection.webSock1.send(JSON.stringify(response))
            },
            // Webソケットが閉じられたとき
            (e)=> {
                console.log(`Socket is closed. Reconnect will be attempted in 1 second. ${e.reason}`)
                // 1回だけ再接続を試みます
                this._reconnect()
            },
            // サーバーからのメッセージを受信したとき
            this._setMessageFromServer,
            // エラー時
            (e)=> {
                console.log(`Socket is error. ${e.reason}`)
            }
        )
        '''

    def onStart(self):
        """開始時"""
        self._winner = ""

        self._position.onStart(self._connection.myPiece)
```
