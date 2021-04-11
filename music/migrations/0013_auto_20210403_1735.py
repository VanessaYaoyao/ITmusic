# Generated by Django 2.2 on 2021-04-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0012_auto_20210401_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='albumcomment',
            options={'ordering': ['-comment_time'], 'verbose_name': '专辑评论信息管理', 'verbose_name_plural': '专辑评论信息管理'},
        ),
        migrations.AlterModelOptions(
            name='listcomment',
            options={'ordering': ['-comment_time'], 'verbose_name': '歌单评论信息管理', 'verbose_name_plural': '歌单评论信息管理'},
        ),
        migrations.AlterModelOptions(
            name='songcomment',
            options={'ordering': ['-comment_time'], 'verbose_name': '歌曲评论信息管理', 'verbose_name_plural': '歌曲评论信息管理'},
        ),
        migrations.AddField(
            model_name='fan',
            name='fan_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='follow_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='fan',
            name='fan',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follow',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
