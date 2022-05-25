from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    # この User オブジェクトの下に Profile オブジェクトをぶら下げると思ってください
    #
    # Example
    # -------
    #
    # user = User.objects.get(pk=user_id)
    # print(user.profile.match_state)
    #
    # OneToOneField - 1対1対応のリレーション。 デフォルトで Unique 属性
    #
    # * `on_delete` - 必須。 models.CASCADE なら、親テーブルのレコードが消されると、子テーブルのレコードも削除されます
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)

    # 対局のマッチング状態
    #
    # * `blank` - 未指定でもセーブを受け入れるなら真
    # * `default` - 初期値
    match_state = models.IntegerField(
        '対局のマッチング状態', null=True, blank=True, default=0)

    def __str__(self):
        """このオブジェクトを文字列にしたとき返るもの"""
        return f"{self.user}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """新規作成"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存"""
    instance.profile.save()


# 📖 [Extending the User model with custom fields in Django](https://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django)
post_save.connect(create_user_profile, sender=User)
