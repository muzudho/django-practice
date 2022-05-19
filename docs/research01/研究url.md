# 研究

📖 [django-allauth/allauth/account/urls.py](https://github.com/pennersr/django-allauth/blob/master/allauth/account/urls.py)  

13 個も API がある？

# (1) account_signup

Path: "signup/"
Call: views.signup
Comment: 

# (2) account_login

Path: "login/"
Call: views.login
Comment: 

# (3) account_logout

Path: "logout/"
Call: views.logout
Comment: 

# (4) account_change_password

Path: "password/change/"
Call: views.password_change
Comment: 

# (5) account_set_password

Path: "password/set/"
Call: views.password_set
Comment: 

# (6) account_inactive

Path: "inactive/"
Call: views.account_inactive
Comment: 

# (7) account_email

Path: "email/"
Call: views.email
Comment: E-mail

# (8) account_email_verification_sent

Path: "confirm-email/"
Call: views.email_verification_sent
Comment: E-mail

# (9) account_confirm_email

Path: r"^confirm-email/(?P<key>[-:\w]+)/$"
Call: views.confirm_email
Comment: E-mail

# (10) account_reset_password

Path: "password/reset/"
Call: views.password_reset
Comment: password reset

# (11) account_reset_password_done

Path: "password/reset/done/"
Call: views.password_reset_done
Comment: password reset

# (12) account_reset_password_from_key

Path: r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$"
Call: views.password_reset_from_key
Comment: password reset

# (13) account_reset_password_from_key_done

Path: "password/reset/key/done/"
Call: views.password_reset_from_key_done
Comment: password reset
