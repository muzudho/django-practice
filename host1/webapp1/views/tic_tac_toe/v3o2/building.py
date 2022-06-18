from webapp1.views.tic_tac_toe.v2 import game_rule
#    ------- --------------------        ---------
#    1       2                           3
# 1. アプリケーション フォルダー名
# 2. ディレクトリー名
# 3. Python ファイル名。拡張子抜き


class Building():
    """建物"""

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

    def getGameoverState(self):
        """対局結果

        勝者 "X", "O" を、勝敗 WIN, DRAW, LOSE, NONE に変換
        """

        if self._winner == game_rule.PC_EMPTY_LABEL:
            return game_rule.GAMEOVER_DRAW
        elif self._winner == vue1.building.connection.myPiece:
            return game_rule.GAMEOVER_WIN
        elif self._winner == self.flipTurn(vue1.building.connection.myPiece):
            return game_rule.GAMEOVER_LOSE

        return game_rule.GAMEOVER_NONE

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
