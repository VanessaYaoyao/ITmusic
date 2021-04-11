# Generated by Django 2.2 on 2021-03-19 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20210318_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumcomment',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='albumreply',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='listcomment',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='listreply',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='songcomment',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.AddField(
            model_name='songreply',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
    ]