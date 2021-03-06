# Generated by Django 2.2 on 2021-04-01 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_auto_20210331_0853'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='albumcomment',
            options={'verbose_name': '专辑评论信息管理', 'verbose_name_plural': '专辑评论信息管理'},
        ),
        migrations.AlterModelOptions(
            name='listcomment',
            options={'verbose_name': '歌单评论信息管理', 'verbose_name_plural': '歌单评论信息管理'},
        ),
        migrations.AlterModelOptions(
            name='songcomment',
            options={'verbose_name': '歌曲评论信息管理', 'verbose_name_plural': '歌曲评论信息管理'},
        ),
        migrations.AlterField(
            model_name='albumcomment',
            name='content',
            field=models.TextField(default='2', max_length=128, verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='listcomment',
            name='content',
            field=models.TextField(max_length=128, verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='listreply',
            name='content',
            field=models.TextField(max_length=128, verbose_name='回复内容'),
        ),
        migrations.AlterField(
            model_name='songcomment',
            name='content',
            field=models.TextField(max_length=128, verbose_name='评论内容'),
        ),
    ]
