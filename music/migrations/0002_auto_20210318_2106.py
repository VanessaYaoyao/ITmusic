# Generated by Django 2.2 on 2021-03-18 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='albumcomment',
            old_name='song',
            new_name='album',
        ),
        migrations.RenameField(
            model_name='listcomment',
            old_name='song',
            new_name='the_list',
        ),
    ]
