# 目的

ゲーム対局サーバーを作ることにした。  
最重要の要件は次の１点。  

* なるべく多くの人がコード編集に参加できるようにしたい

関わる人は 人工知能分野で、機械学習をしている人が多い。  
そこで **Python** 、 **Django** を選んだ。  

以下は自分用に追加で課したもの

* 会員制のWebサイトにする
* Docker を使う

# ここは目次

学習コストが低くなるように並べている。  
数字の小さな Lesson から　上から下へ１つずつ、飛ばさず全部　読み進めてほしい。  

Table of Contents

* 📖 `DjangoとDockerでゲーム対局サーバーを作ろう！` (この記事)  

Lesson 1. Install  

* 📖 [DjangoをDockerコンテナへインストールしよう！](https://qiita.com/muzudho1/items/48e69ed17d70a8f171a7)  

Lesson 2. Auth  


* 📖 [Djangoでユーザー認証を付けよう！](https://qiita.com/muzudho1/items/55cb7ac55299afd51887)
  * もっと勉強したい人向けの関連記事
    * 📚 [Djangoで、django-allauthのテンプレートを差し替えよう！](https://qiita.com/muzudho1/items/6120055b2a8eb4e28527)
* 📖 [Djangoでサインイン（利用開始）のページを作ろう！](https://qiita.com/muzudho1/items/1d34d64562ff07f1742a)

Lesson 3. Page  

* 📖 [DjangoでWebページを追加しよう！](https://qiita.com/muzudho1/items/06fe071c1147b4b8f062)
* 📖 [Djangoでログイン／ログアウト機能を付けよう！](https://qiita.com/muzudho1/items/9f1ae4d0debc0b8aa4b1)

Lesson 4. Super-user  

* 📖 [Djangoでスーパーユーザーを追加しよう！](https://qiita.com/muzudho1/items/cf21fa75e23e1f987153)

Lesson 5. Model  

* 📖 [Djangoでモデルを追加しよう！](https://qiita.com/muzudho1/items/2463cc006da69f5ed7b2)

Lesson 6. CRUD  

* 📖 [Djangoでモデルのインスタンスの一覧表示をしよう！](https://qiita.com/muzudho1/items/77668130b6d941596327)
    * 📖 [Djangoでモデルのインスタンスの読取ページを作成しよう！](https://qiita.com/muzudho1/items/ae362f53a670e265a7e4)
    * 📖 [Djangoでモデルのインスタンスの削除ページを作成しよう！](https://qiita.com/muzudho1/items/32694c883331c75ef059)
    * 📖 [Djangoでモデルのインスタンスの作成／更新ページを作成しよう！](https://qiita.com/muzudho1/items/806ecdba1654ae169f37)

Lesson 7. Vuetify

* 📖 [DjangoでフロントエンドにVuetifyを使おう！](https://qiita.com/muzudho1/items/e80a72b027249daa4d41)
    * 📖 [DjangoでVuetifyのData tableを使おう！](https://qiita.com/muzudho1/items/2b01d3acce5ec1b5770b)

Lesson 8. JSON

* 📖 [Djangoで動的生成するHTMLの中のJavaScriptにJSONを埋め込もう！](https://qiita.com/muzudho1/items/b3b0c25fc329eb9bc0c1)
    * 📖 [DjangoのWebページへJSON形式のテキストを渡そう！](https://qiita.com/muzudho1/items/c50859d9bde800d06a62)
* 📖 [DjangoのサーバーからデータをJSON形式のテキストで受信しよう！](https://qiita.com/muzudho1/items/d83760a6a4abadaf19c4)
* 📖 [DjangoでデータをサーバーへJSON形式で渡して、記憶させよう！](https://qiita.com/muzudho1/items/ed0ea262aaa327a2d12b)

Lesson 9. Socket

* 📖 [ソケットを使おう！](https://qiita.com/muzudho1/items/7a6501f7dbafbaa9b96c)

Lesson 10. Web socket

* 📖 [DjangoのWebサーバーとクライアント側のアプリで通信しよう！](https://qiita.com/muzudho1/items/9bad88a4092bf83a0f12)
    * 📖 [DjangoのWebサーバーとクライアント側のアプリ間でJSON形式のテキストを通信しよう！](https://qiita.com/muzudho1/items/a3870c78f609a65debe0)

Lesson 11. Tic tac toe

* 📖 [Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！](https://qiita.com/muzudho1/items/3bd5e55fbea2c0598e8b)
    * 📖 [Djangoを介してWebブラウザ越しに２人対戦できる〇×ゲームを作ろう！ Vuetify編](https://qiita.com/muzudho1/items/f302bdb40fb5c13f9603)

Lesson 12. Open server

* 📖 [Django さくらVPS 備忘録](https://qiita.com/muzudho1/items/1d3b4b5608716463184c)

Lesson 13. Make room

* 📖 [Djangoでゲーム対局部屋を登録しよう！](https://qiita.com/muzudho1/items/e1cf253dd6929bcd708d)
* 📖 [Djangoでゲーム対局部屋を一覧しよう！](https://qiita.com/muzudho1/items/346c286d4f99850afe23)
* 📖 [Djangoでゲーム対局部屋を読取しよう！](https://qiita.com/muzudho1/items/a39bea2f098951292916)
* 📖 [Djangoでゲーム対局部屋を削除しよう！](https://qiita.com/muzudho1/items/172485842e7adfb749aa)
* 📖 [Djangoでゲーム対局部屋を作成または更新しよう！](https://qiita.com/muzudho1/items/6eaf6cf90fe5a6519184)

Lesson 14. Portal

* 📖 [Djangoでゲームポータルページを作ろう！](https://qiita.com/muzudho1/items/0c59f3ce7aa6bef2a91f)

Lesson 15. User home

* 📖 [Djangoでユーザーホームを作ろう！](https://qiita.com/muzudho1/items/37532c83235b7f9e60c9)

Lesson 16. Active user

* 📖 [Djangoでアクティブユーザーの一覧を作ろう！](https://qiita.com/muzudho1/items/bea77e8a69c5c805e1d7)

Lesson 17. Lobby

* 📖 [Djangoでロビー（待合室）を作ろう！](https://qiita.com/muzudho1/items/57677b07854aca71b42d)

Lesson 18. Users

* 📖 [Djangoで会員登録ユーザーを一覧しよう！](https://qiita.com/muzudho1/items/13c15be5b9070dab1770)

Lesson 19. Matching automatically

* 📖 [Djangoで自動リロードするページを作ろう！](https://qiita.com/muzudho1/items/8df599dc0e0acb25f649)
