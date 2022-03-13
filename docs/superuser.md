# スーパーユーザーの作成

以下のようにディレクトリとファイルを作成してほしい。  

```plaintext
📂host1
　└── 📂webapp1
　 　　└── 📂management
    　 　　└── 📂commands
                └── 📄custom_createsuperuser.py
```

📄host1/webapp1/management/commands/custom_createsuperuser.py  

```py
# See also: https://jumpyoshim.hatenablog.com/entry/how-to-automate-createsuperuser-on-django
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Create a superuser with a password non-interactively'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        username = options.get('username')
        email = options.get('email')
        password = options.get('password')
        database = options.get('database')

        if not (username and email and password):
            raise CommandError('--username, --email and --password are required options')

        user_data = {
            'username': username,
            'email': email,
            'password': password,
        }

        exists = self.UserModel._default_manager.db_manager(database).filter(username=username).exists()
        if not exists:
            self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
```

Dockerコンテナを停止してほしい。  

次に以下のコマンドを打鍵してほしい。Dockerコンテナの中で動いているサーバーアプリケーションにスーパーユーザーが追加される。タイプミスしないように注意してほしい。  

```shell
docker-compose run --rm web python3 manage.py custom_createsuperuser --username <スーパーユーザー名> --email <スーパーユーザーのEmailアドレス> --password <スーパーユーザーのパスワード>
```

👆 `docker-compose up` したときに実行してくれれば良いんだが、方法が分からなかった。  
Dockerコンテナの破棄～起動のたびに打鍵するのがめんどくさければ .env に `#` 行頭コメント印を付けてメモ書きしておくといいだろう。  

以下のコマンドを打鍵してほしい。  

```shell
docker-compose up
```

# Webの管理画面へアクセス

📖 [http://localhost:8000/admin](http://localhost:8000/admin)  

# 参考にした記事

📖 [Django 管理画面の利用](https://python.keicode.com/django/admin-site-enabling.php)  
📖 [【Django】ワンライナーでスーパーユーザーを作成する方法](https://jumpyoshim.hatenablog.com/entry/how-to-automate-createsuperuser-on-django)  
