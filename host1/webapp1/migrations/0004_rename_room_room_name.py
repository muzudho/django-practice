# Generated by Django 3.2.12 on 2022-05-10 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp1', '0003_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room',
            new_name='name',
        ),
    ]
