from django.contrib import admin
from .models import Song,Album,User,AllLists,TheList,Fan,Follow,LikeAlbums,LikeLists,LikeSongs,AlbumComment,SongComment,ListComment,AlbumReply,SongReply,ListReply

# Register your models here.
@admin.register(User)
class Users(admin.ModelAdmin):
    list_display = ['username','email','avatar']
    search_fields = ('username','email')

@admin.register(Song)
class Songs(admin.ModelAdmin):
    list_display = ['song_name','play_count']
    search_fields = ('song_name',)

@admin.register(Album)
class Albums(admin.ModelAdmin):
    list_display = ['album_name','singer']
    search_fields = ('album_name',)

@admin.register(AllLists)
class AllLists(admin.ModelAdmin):
    list_display = ['list_name','user']
    search_fields = ('list_name',)

@admin.register(TheList)
class ListSong(admin.ModelAdmin):
    list_display = ['song']
    search_fields = ('id',)

@admin.register(Fan)
class Fans(admin.ModelAdmin):
    list_display = ['fan_id']
@admin.register(Follow)
class Follow(admin.ModelAdmin):
    list_display = ['follow_id']

@admin.register(LikeSongs)
class SongLike(admin.ModelAdmin):
    list_display = ['id']

@admin.register(LikeLists)
class ListLike(admin.ModelAdmin):
    list_display = ['id']

@admin.register(LikeAlbums)
class AlbumLike(admin.ModelAdmin):
    list_display = ['id']

@admin.register(SongComment)
class SongComments(admin.ModelAdmin):
    list_display = ['id','content']


@admin.register(AlbumComment)
class AlbumComments(admin.ModelAdmin):
    list_display = ['id','content']


@admin.register(ListComment)
class ListComments(admin.ModelAdmin):
    list_display = ['id','content']



