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
        │   ├── 📄asgi.py
        │   ├── 📄routing1.py
        │   ├── 📄settings.py
        │   ├── 📄urls.py
        │   └── 📄<いろいろ>
        ├── 📄.env
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

# Step 2. ゲームルール定義 - game_rule.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      └── 📄game_rule.py
```

```py
# ゲームオーバー判定
#
# * 自分視点
GAMEOVER_NONE = 0
"""ゲームオーバーしてません"""

GAMEOVER_WIN = 1
"""勝ち"""

GAMEOVER_DRAW = 2
"""引き分け"""

GAMEOVER_LOSE = 3
"""負け"""

# PC は Piece （駒、石、などの意味）の略です。
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

WIN_PATTERN = [
    [SQ_0, SQ_1, SQ_2],
    """
    +---------+
    | *  *  * |
    | .  .  . |
    | .  .  . |
    +---------+
    """

    [SQ_3, SQ_4, SQ_5],
    """
    +---------+
    | .  .  . |
    | *  *  * |
    | .  .  . |
    +---------+
    """

    [SQ_6, SQ_7, SQ_8],
    """
    +---------+
    | .  .  . |
    | .  .  . |
    | *  *  * |
    +---------+
    """

    [SQ_0, SQ_3, SQ_6],
    """
    +---------+
    | *  .  . |
    | *  .  . |
    | *  .  . |
    +---------+
    """

    [SQ_1, SQ_4, SQ_7],
    """
    +---------+
    | .  *  . |
    | .  *  . |
    | .  *  . |
    +---------+
    """

    [SQ_2, SQ_5, SQ_8],
    """
    +---------+
    | .  .  * |
    | .  .  * |
    | .  .  * |
    +---------+
    """

    [SQ_0, SQ_4, SQ_8],
    """
    +---------+
    | *  .  . |
    | .  *  . |
    | .  .  * |
    +---------+
    """

    [SQ_2, SQ_4, SQ_6],
    """
    +---------+
    | .  .  * |
    | .  *  . |
    | *  .  . |
    +---------+
    """
]
"""石が３つ並んでいるパターン"""


def flipTurn(piece):
    """手番反転

    Returns
    -------
    str
        piece
    """

    if piece == PC_X_LABEL:
        return PC_O_LABEL
    elif piece == PC_O_LABEL:
        return PC_X_LABEL

    return piece
```

# Step 3. 遊具定義 - playground_equipment.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄game_rule.py
👉                      └── 📄playground_equipment.py
```

```py
from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class PlaygroundEquipment():
    """遊具"""

    def __init__(self):
        # あとで onStart(...) を呼出してください
        pass

    def onStart(self, myPiece):
        """対局開始時

        Parameters
        ----------
        myPiece : str
            "X", "O", "_"
        """

        self._board = [game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY,
                       game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY, game_rule.PC_EMPTY]
        """盤面"""

        self._countOfMove = 0
        """何手目"""

        self._isMyTurn = myPiece == game_rule.PC_X_LABEL
        """自分の手番か（初回は先手）"""

        self._isVisibleAlertWaitForOther = False
        """「相手の手番に着手しないでください」というアラートの可視性"""

        self._gameoverState = game_rule.GAMEOVER_NONE
        """ゲームオーバーしてません"""

        # イベントハンドラはそのまま

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
        return self._board[sq]

    def setPiece(self, sq, piece):
        """盤上のマスに駒を上書きします

        Parameters
        ----------
        sq : int
            マス番号
        piece : str
            駒
        """
        self._board[sq] = piece

    def incrementCountOfMove(self):
        """手数を１増やします"""
        self._countOfMove += 1

    def isBoardFill(self):
        """マスがすべて埋まっていますか"""
        return self._countOfMove == 9

    def isThere3SamePieces(self):
        """同じ駒が３個ありますか"""
        return 5 <= self._countOfMove

    @property
    def isMyTurn(self):
        """私のターンですか"""
        return self._isMyTurn

    @isMyTurn.setter
    def isMyTurn(self, value):
        self._isMyTurn = value

    @property
    def isVisibleAlertWaitForOther(self):
        """「相手の手番に着手しないでください」というアラートの可視性"""
        return self._isVisibleAlertWaitForOther

    @isVisibleAlertWaitForOther.setter
    def isVisibleAlertWaitForOther(self, value):
        self._isVisibleAlertWaitForOther = value

    @property
    def gameoverState(self):
        """ゲームオーバー状態"""
        return self._gameoverState

    @gameoverState.setter
    def gameoverState(self, value):
        self._gameoverState = value
```

# Step 4. ユーザー操作定義 - user_ctrl.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄game_rule.py
                        ├── 📄playground_equipment.py
👉                      └── 📄user_ctrl.py
```

```py
from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class UserCtrl ():
    """ユーザーコントロール"""

    def __init__(self, playeq):
        """_summary_

        Parameters
        ----------
        playeq : _type_
            遊具
        """

        self._playeq = playeq
        """遊具"""

        def doNothing():
            pass

        self._onDoMove = doNothing
        """イベントリスナー"""

    @property
    def onDoMove(self):
        return self._onDoMove

    @onDoMove.setter
    def onDoMove(self, value):
        """石を置いたとき"""
        self._onDoMove = value

    def doMove(self, sq, piece):
        """石を置きます

        Parameters
        ----------
        sq : int
            升番号 0 <= sq
        piece : str
            X か O

        Returns
        -------
        _type_
            石を置けたら真、それ以外は偽
        """
        if self._playeq.gameoverState != game_rule.GAMEOVER_NONE:
            # Warning of illegal move
            print(
                f"Warning of illegal move. gameoverState={self._playeq.gameoverState}")

        if self._playeq.getPieceBySq(sq) == game_rule.PC_EMPTY:
            # 空升なら

            self._playeq.incrementCountOfMove()
            # 手数を１増やします

            # 石を置きます
            if piece == game_rule.PC_X_LABEL:
                self._playeq.setPiece(sq, game_rule.PC_X)
            elif piece == game_rule.PC_O_LABEL:
                self._playeq.setPiece(sq, game_rule.PC_O)
            else:
                print(f"[Error] Invalid piece={piece}")
                return False

            print(f"[UserCtrl doMove] sq={sq} piece={piece}")
            self._onDoMove(sq, piece)

        return True
```

# Step 5. 審判操作定義 - judge_ctrl.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
                        ├── 📄game_rule.py
👉                      ├── 📄judge_ctrl.py
                        ├── 📄playground_equipment.py
                        └── 📄user_ctrl.py
```

```py
from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class JudgeCtrl():
    """審判コントロール"""

    def __init__(self, playeq, userCtrl):
        """生成

        Parameters
        ----------
        playeq:
            遊具
        userCtrl:
            ユーザーコントロール
        """

        self._playeq = playeq
        """遊具"""

        self._userCtrl = userCtrl
        """ユーザーコントロール"""

        def doNothing():
            pass

        self._onWon = doNothing
        """イベントリスナー"""

        self._onDraw = doNothing

    def onWon(self, func):
        """勝ったとき"""
        self._onWon = func

    def onDraw(self, func):
        """引き分けたとき"""
        self._onDraw = func

    def doJudge(self, myPiece):
        """ゲームオーバー判定"""

        self._playeq.gameoverState = self.makeGameoverSet()
        print(f"[doJudge] gameoverState={self._playeq.gameoverState}")

        if self._playeq.gameoverState == game_rule.GAMEOVER_WIN:
            self._onWon(myPiece)
        elif self._playeq.gameoverState == game_rule.GAMEOVER_DRAW:
            self._onDraw()
        elif self._playeq.gameoverState == game_rule.GAMEOVER_LOSE:
            pass
        elif self._playeq.gameoverState == game_rule.GAMEOVER_NONE:
            pass
        else:
            raise ValueError(
                f"Unexpected gameoverState={self._playeq.gameoverState}")

    def makeGameoverSet(self):
        """ゲームオーバー判定

        * 自分が指した後の盤面（＝手番が相手に渡った始めの盤面）を評価することに注意してください

        Returns
        -------
        ゲームオーバー状態
        """
        print(
            f"[makeGameoverSet] isThere3SamePieces={self._playeq.isThere3SamePieces()}")
        if self._playeq.isThere3SamePieces():
            for squaresOfWinPattern in game_rule.WIN_PATTERN:
                print(
                    f"[makeGameoverSet] self.isPieceInLine(squaresOfWinPattern)={self.isPieceInLine(squaresOfWinPattern)}")
                if self.isPieceInLine(squaresOfWinPattern):
                    print(
                        f"[makeGameoverSet] self._playeq.myTurn.isTrue={self._playeq.myTurn.isTrue}")
                    if self._playeq.myTurn.isTrue:
                        # 相手が指して自分の手番になったときに ３目が揃った。私の負け
                        return game_rule.GAMEOVER_LOSE
                    else:
                        # 自分がが指して相手の手番になったときに ３目が揃った。私の勝ち
                        return game_rule.GAMEOVER_WIN

        if self._playeq.isBoardFill():
            # 勝ち負けが付かず、盤が埋まったら引き分け
            return game_rule.GAMEOVER_DRAW

        # ゲームオーバーしてません
        return game_rule.GAMEOVER_NONE

    def isPieceInLine(self, squaresOfWinPattern):
        """駒が３つ並んでいるか？

        Parameters
        ----------
        squaresOfWinPattern : _type_
            勝ちパターン

        Returns
        -------
        _type_
            並んでいれば真、それ以外は偽
        """
        return self._playeq.getPieceBySq(squaresOfWinPattern[0]) != game_rule.PC_EMPTY and \
            self._playeq.getPieceBySq(squaresOfWinPattern[0]) == self._playeq.getPieceBySq(squaresOfWinPattern[1]) \
            and self._playeq.getPieceBySq(squaresOfWinPattern[0]) == self._playeq.getPieceBySq(squaresOfWinPattern[2])
```

# Step 6. エンジン作成 - engine.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂views
                └── 📂tic-tac-toe
                    └── 📂v2
👉                      ├── 📄engine.py
                        ├── 📄game_rule.py
                        ├── 📄judge_ctrl.py
                        ├── 📄playground_equipment.py
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

        self._playeq = PlaygroundEquipment()
        """遊具"""

        self._userCtrl = UserCtrl(self._playeq)
        """ユーザーコントロール"""

        self._judgeCtrl = JudgeCtrl(self._playeq, self._userCtrl)
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
        """遊具"""
        return self._playeq

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
        elif self._winner == vue1.engine.connection.myPiece:
            return GameoverSet.win
        elif self._winner == self.flipTurn(vue1.engine.connection.myPiece):
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

        self._playeq.onStart(self._connection.myPiece)
```
