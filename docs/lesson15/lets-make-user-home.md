
# Step 5. 設定編集 - settings.py ファイル

以下のファイルを編集してほしい。  

```plaintext
    └── 📂host1
        ├── 📂webapp1                       # アプリケーション フォルダー
        │   ├── 📂templates
        │   │   └── 📂webapp1               # アプリケーション フォルダーと同じ名前
        │   │       └── 📂home
        │   │           └── 📂v1
        │   │               └── 📄home.html
        │   ├── 📂views
        │   │   └── 📄v_home.py
        │   └── 📄urls.py
👉      └── 📄settings.py
```

```py
# (Old) LOGIN_REDIRECT_URL = 'home'  # ログイン後に遷移するURLの指定
LOGIN_REDIRECT_URL = 'homeV1_home'  # ログイン後に遷移するURLの指定
```

# Step 6. Web画面へアクセス

📖 [http://localhost:8000/home/v1/](http://localhost:8000/home/v1/)  

# 次の記事

📖 [Djangoでアクティブユーザーの一覧を作ろう！](https://qiita.com/muzudho1/items/bea77e8a69c5c805e1d7)  
