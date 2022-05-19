# django-allauthを解析しよう！

DjangoでWebサイトを作ったとき、会員登録めんどくさいから SNSのアカウントでログインしたい、  
というときの選択肢として django-allauth は重要なわりに、記事が少ない。無いなら自分でまとめよう。  

作者がソースを大幅にいじったら わたしの記事は全部無駄になるが、現時点の django-allauth のソースを解析していこう。  

## まず urls.py を見ろ

📖 [django-allauth/allauth/account/urls.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/urls.py)  

|  Num | Name                                 | Path                                                            | View object                            |
| ---: | ------------------------------------ | --------------------------------------------------------------- | -------------------------------------- |
|    1 | account_signup                       | `signup/`                                                       | views.**signup**                       |
|    2 | account_login                        | `login/`                                                        | views.**login**                        |
|    3 | account_logout                       | `logout/`                                                       | views.**logout**                       |
|    4 | account_change_password              | `password/change/`                                              | views.**password_change**              |
|    5 | account_set_password                 | `password/set/`                                                 | views.**password_set**                 |
|    6 | account_inactive                     | `inactive/`                                                     | views.**account_inactive**             |
|    7 | account_email                        | `email/`                                                        | views.**email**                        |
|    8 | account_email_verification_sent      | `confirm-email/`                                                | views.**email_verification_sent**      |
|    9 | account_confirm_email                | `r"^confirm-email/(?P<key>[-:\w]+)/$"`                          | views.**confirm_email**                |
|   10 | account_reset_password               | `password/reset/`                                               | views.**password_reset**               |
|   11 | account_reset_password_done          | `password/reset/done/`                                          | views.**password_reset_done**          |
|   12 | account_reset_password_from_key      | `r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$"` | views.**password_reset_from_key**      |
|   13 | account_reset_password_from_key_done | `password/reset/key/done/`                                      | views.**password_reset_from_key_done** |

👆 URLにアクセスすれば、 URLの形に合った、Viewオブジェクトの get なり post なりのメソッドが呼び出される仕組みだ  

## 次に views.py を見ろ

📖 [django-allauth/allauth/account/views.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py)  

|  Num | Create instance                                                       | Class                        |
| ---: | --------------------------------------------------------------------- | ---------------------------- |
|    1 | signup = SignupView.as_view()                                         | SignupView                   |
|    2 | login = LoginView.as_view()                                           | LoginView                    |
|    3 | logout = LogoutView.as_view()                                         | LogoutView                   |
|    4 | password_change = login_required(PasswordChangeView.as_view())        | PasswordChangeView           |
|    5 | password_set = login_required(PasswordSetView.as_view())              | PasswordSetView              |
|    6 | account_inactive = AccountInactiveView.as_view()                      | AccountInactiveView          |
|    7 | email = login_required(EmailView.as_view())                           | EmailView                    |
|    8 | email_verification_sent = EmailVerificationSentView.as_view()         | EmailVerificationSentView    |
|    9 | confirm_email = ConfirmEmailView.as_view()                            | ConfirmEmailView             |
|   10 | password_reset = PasswordResetView.as_view()                          | PasswordResetView            |
|   11 | password_reset_done = PasswordResetDoneView.as_view()                 | PasswordResetDoneView        |
|   12 | password_reset_from_key = PasswordResetFromKeyView.as_view()          | PasswordResetFromKeyView     |
|   13 | password_reset_from_key_done = PasswordResetFromKeyDoneView.as_view() | PasswordResetFromKeyDoneView |

👆 URL に対応する クラス名までは分かった  

## テンプレート名を見ろ

以上のクラスは `template_name` プロパティを持っている  

|  Num | Class                        | template_name                                                               |
| ---: | ---------------------------- | --------------------------------------------------------------------------- |
|    1 | SignupView                   | `"account/signup." + app_settings.TEMPLATE_EXTENSION`                       |
|    2 | LoginView                    | `"account/login." + app_settings.TEMPLATE_EXTENSION`                        |
|    3 | LogoutView                   | `"account/logout." + app_settings.TEMPLATE_EXTENSION`                       |
|    4 | PasswordChangeView           | `"account/password_change." + app_settings.TEMPLATE_EXTENSION`              |
|    5 | PasswordSetView              | `"account/password_set." + app_settings.TEMPLATE_EXTENSION`                 |
|    6 | AccountInactiveView          | `"account/account_inactive." + app_settings.TEMPLATE_EXTENSION`             |
|    7 | EmailView                    | `"account/email_confirm." + app_settings.TEMPLATE_EXTENSION`                |
|    8 | EmailVerificationSentView    | `"account/verification_sent." + app_settings.TEMPLATE_EXTENSION`            |
|    9 | ConfirmEmailView             | `"account/email_confirm." + app_settings.TEMPLATE_EXTENSION`                |
|   10 | PasswordResetView            | `"account/password_reset." + app_settings.TEMPLATE_EXTENSION`               |
|   11 | PasswordResetDoneView        | `"account/password_reset_done." + app_settings.TEMPLATE_EXTENSION`          |
|   12 | PasswordResetFromKeyView     | `"account/password_reset_from_key." + app_settings.TEMPLATE_EXTENSION`      |
|   13 | PasswordResetFromKeyDoneView | `"account/password_reset_from_key_done." + app_settings.TEMPLATE_EXTENSION` |

👆template_name プロパティを見れば、HTML（のようなもの）のファイルがどこに格納されているか当たりが付く  

## テンプレートを見ろ

📖 [django-allauth/allauth/templates/account](https://github.com/pennersr/django-allauth/tree/master/allauth/templates/account)  

👆 テンプレートが置いてあることを確認してほしい。こんな記事を読む人間は、この HTML がダサいから Vuetify に置き換えたい、といったところだろう  
