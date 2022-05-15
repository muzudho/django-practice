
# Step 2. モデル関連作成 - m_state_in_park.py ファイル

以下のファイルを新規作成してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models
👉              └── 📄m_state_in_park.py
```

```py
from enum import Enum


class StateInPark(Enum):
    """状態1"""

    # その他
    NONE = 0

    # 対局中
    DURING_GAME = 1
```

# Step 2. モデル編集 - m_member.py ファイル

以下のファイルに、フィールドを追加してほしい  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            └── 📂models
                ├── 📄m_state_in_park.py
👉              └── 📄m_member.py
```

抜粋

```py
    # 既存の行
    name = models.CharField('氏名', max_length=255)
    email = models.CharField('E-Mail', max_length=255)
    age = models.IntegerField('年齢', blank=True, default=0)

    # 追加してほしい
    stateInPark = models.IntegerField('状態1', blank=False, default=0)
```

# Step 3. モデル作成 - コマンド実行

```shell
cd host1

docker-compose run --rm web python3 manage.py makemigrations webapp1
#                                                            -------
#                                                            1
# 1. アプリケーション ディレクトリー名
```

以下のディレクトリーとファイルが生成される。  

```plaintext
    └── 📂host1
        └── 📂webapp1                       # アプリケーション フォルダー
            ├── 📂migrations
            │   ├── 📄<いろいろ>.py
👉          │   └── 📄0004_member_stateinpark.py    # 差分。ファイル名は違うかもしれない
            └── 📂models
                ├── 📄m_state_in_park.py
                └── 📄m_member.py
```

👆 これらのファイルは マイグレーション ファイル と呼ぶらしい。  

# Step 4. モデル作成 - コマンド実行＜その２＞

```shell
docker-compose run --rm web python manage.py migrate
```

👆 ここまでやって マイグレーション という作業が終わるらしい。  
