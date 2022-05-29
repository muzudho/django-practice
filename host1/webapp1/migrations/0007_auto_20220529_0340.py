# Generated by Django 3.2.12 on 2022-05-29 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp1', '0006_alter_profile_match_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='gote_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='対局者_後手Id'),
        ),
        migrations.AddField(
            model_name='room',
            name='sente_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='対局者_先手Id'),
        ),
    ]
