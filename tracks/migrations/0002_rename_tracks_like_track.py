# Generated by Django 3.2 on 2021-05-01 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='tracks',
            new_name='track',
        ),
    ]