from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True, verbose_name='头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    follow_count = models.IntegerField(default=0,verbose_name='关注数')
    fan_count = models.IntegerField(default=0,verbose_name='粉丝数')
    description = models.TextField(default='',verbose_name='简介',blank=True)
    gender = models.CharField(default='',max_length=128,verbose_name='性别',blank=True)
    address = models.CharField(default='',max_length=128,verbose_name='地址',blank=True)
    age = models.IntegerField(default=0,verbose_name='年龄',blank=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = '用户信息管理'
        verbose_name_plural = verbose_name

class Album(models.Model):

    album_name = models.CharField(max_length=128,verbose_name='专辑名')
    album_picture = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True,verbose_name='专辑封面')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='上架时间')
    singer = models.CharField(max_length=128,verbose_name='歌手')
    description = models.TextField(verbose_name='专辑简介',default='')
    banner = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True,verbose_name='专辑轮播图')
    def __str__(self):
        return str(self.album_name)

    class Meta:
        verbose_name = '专辑信息管理'
        verbose_name_plural = verbose_name
        ordering = ['-upload_time']

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None

            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            data[f.name] = value
        return data


class Song(models.Model):
    song_name = models.CharField(max_length=128,verbose_name='歌曲名')
    song_url = models.FileField(upload_to='song/%Y%m%d/',verbose_name='歌曲资源')
    play_count = models.IntegerField(default=0, verbose_name='播放量')
    lyric = models.FileField(upload_to='song/lyric/%Y%m%d',verbose_name='歌词',blank=True)
    album = models.ForeignKey('Album',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.song_name)

    class Meta:
        verbose_name = '歌曲信息管理'
        verbose_name_plural = verbose_name
        ordering = ['-play_count']

class SongComment(models.Model):
    content = models.TextField(max_length=128,verbose_name='评论内容')
    sender = models.CharField(max_length=128,verbose_name='评论人',blank=True)
    sender_id = models.IntegerField(null=True,verbose_name='评论人id')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    like_count = models.IntegerField(default=0,verbose_name='点赞数')
    song = models.ForeignKey('Song',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '歌曲评论信息管理'
        verbose_name_plural = verbose_name
        ordering = ['-comment_time']

class SongCommentLike(models.Model):
    comment=models.ForeignKey('SongComment',on_delete=models.CASCADE)
    user = models.ForeignKey('User',on_delete=models.CASCADE)

class SongReply(models.Model):
    content = models.CharField(max_length=128,verbose_name='回复内容')
    replier = models.CharField(max_length=128,verbose_name='回复人')
    reply_time = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    comment = models.ForeignKey('SongComment',on_delete=models.CASCADE)

class ListComment(models.Model):
    content = models.TextField(max_length=128,verbose_name='评论内容')
    sender = models.CharField(max_length=128,verbose_name='评论人',blank=True)
    sender_id = models.IntegerField(null=True, verbose_name='评论人id')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    the_list = models.ForeignKey('AllLists',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '歌单评论信息管理'
        verbose_name_plural = verbose_name
        ordering = ['-comment_time']
class ListCommentLike(models.Model):
    comment = models.ForeignKey('ListComment',on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class ListReply(models.Model):
    content = models.TextField(max_length=128,verbose_name='回复内容')
    replier = models.CharField(max_length=128,verbose_name='回复人')
    reply_time = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    comment = models.ForeignKey('ListComment',on_delete=models.CASCADE)

class AlbumComment(models.Model):
    content = models.TextField(max_length=128,verbose_name='评论内容',default='2')
    sender = models.CharField(max_length=128,verbose_name='评论人',blank=True)
    sender_id = models.IntegerField(null=True, verbose_name='评论人id')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    album = models.ForeignKey('Album',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '专辑评论信息管理'
        verbose_name_plural = verbose_name
        ordering = ['-comment_time']

class AlbumCommentLike(models.Model):
    comment = models.ForeignKey('AlbumComment',on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

class AlbumReply(models.Model):
    content = models.CharField(max_length=128,verbose_name='回复内容')
    replier = models.CharField(max_length=128,verbose_name='回复人')
    reply_time = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    comment = models.ForeignKey('AlbumComment',on_delete=models.CASCADE)

class AllLists(models.Model):
    list_name = models.CharField(max_length=128,verbose_name='歌单名')
    song_count = models.IntegerField(default=0,verbose_name='歌曲数')
    list_picture = models.ImageField (upload_to='avatar/%Y%m%d/', blank=True,verbose_name='歌单封面')
    description = models.TextField(verbose_name='歌单简介',default='',blank=True)
    user = models.ForeignKey('User',on_delete=models.CASCADE,verbose_name='创建者')
    play_count = models.IntegerField(default=0,verbose_name='播放量')
    upload_time = models.DateTimeField(auto_now_add=True,null=True,verbose_name='上架时间')

    def __str__(self):
        return str(self.list_name)

    class Meta:
        verbose_name = '歌单信息管理'
        verbose_name_plural = verbose_name
        ordering = ['-play_count']


class TheList(models.Model):
    all_lists = models.ForeignKey('AllLists',on_delete=models.CASCADE)
    song = models.ForeignKey('Song',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '歌单歌曲信息管理'
        verbose_name_plural = verbose_name

class LikeSongs(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    song = models.ForeignKey('Song',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '喜爱歌曲信息管理'
        verbose_name_plural = verbose_name

class LikeAlbums(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    album = models.ForeignKey('Album',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '喜爱专辑信息管理'
        verbose_name_plural = verbose_name
class LikeLists(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    list = models.ForeignKey('AllLists',on_delete=models.CASCADE)
    class Meta:
        verbose_name = '喜爱歌单信息管理'
        verbose_name_plural = verbose_name
class Follow(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    follow = models.CharField(max_length=128, blank=True)
    follow_id = models.IntegerField(null=True)
    class Meta:
        verbose_name = '用户关注信息管理'
        verbose_name_plural = verbose_name

class Fan(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    fan = models.CharField(max_length=128,blank=True)
    fan_id = models.IntegerField(null=True)
    class Meta:
        verbose_name = '用户粉丝信息管理'
        verbose_name_plural = verbose_name

class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10,
                                 choices=(("register", u"注册"), ("forget", u"找回密码")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", auto_now_add=True)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)