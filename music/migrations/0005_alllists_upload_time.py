# Generated by Django 2.2 on 2021-03-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_album_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='alllists',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='上架时间'),
        ),
    ]
