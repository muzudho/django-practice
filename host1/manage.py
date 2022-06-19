#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # * 設定ファイル `host1/webapp1/settings.py` は `host1/settings.py` へ移動した
    # * 変更前
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp1.settings')
    #
    # * 変更後
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

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
