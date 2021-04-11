from django.urls import path
from . import views


urlpatterns = [
    path('itmusic/index', views.index,name='index'),
    path('itmusic/top/songs',views.top_songs,name='top_songs'),
    path('itmusic/top/albums',views.top_albums,name='top_albums'),
    path('itmusic/top/playlists',views.top_lists,name='top_lists'),
    path('itmusic/register', views.register,name='register'),
    path('itmusic/verify',views.verify,name='verify'),
    path('itmusic/findback',views.findback,name='findback'),
    path('itmusic/reset',views.reset,name='reset'),
    path('itmusic/login',views.login,name='login'),
    path('itmusic/logout',views.logout,name='logout'),
    path('itmusic/userinfo',views.userinfo,name='userinfo'),
    path('itmusic/search',views.search,name='search'),
    path('itmusic/song/detail',views.check_song,name='song'),
    path('itmusic/collect_song',views.collect_song,name='collect_song'),
    path('itmusic/addin_playlist',views.addin_playlist,name='addin_playlist'),
    path('itmusic/comment/song',views.song_comment,name='song_comment'),
    path('itmusic/album/detail',views.check_album,name='album'),
    path('itmusic/collect_album',views.collect_album,name='collect_album'),
    path('itmusic/comment/album',views.album_comment,name='album_comment'),
    path('itmusic/playlist/detail',views.check_list,name='list'),
    path('itmusic/collect_playlist',views.collect_playlist,name='collect_playlist'),
    path('itmusic/comment/playlist',views.list_comment,name='list_comment'),
    path('itmusic/user/account',views.account,name='account'),
    path('itmusic/user/detail',views.check_user,name='user'),
    path('itmusic/follow',views.follow,name='follow'),
    path('itmusic/user/songs',views.user_songs,name='user_songs'),
    path('itmusic/user/albums',views.user_albums,name='user_albums'),
    path('itmusic/user/playlists',views.user_lists,name='user_lists'),
    path('itmusic/banner',views.banner,name='banner'),
    path('itmusic/change_password',views.change_password,name='change_password'),
    path('itmusic/create_list',views.create_list,name='create_list'),
    path('itmusic/delete_list',views.delete_list,name='delete_list'),
    path('itmusic/comment_like/song',views.com_like_song,name='com_like_song'),
    path('itmusic/comment_like/album',views.com_like_album,name='com_like_album'),
    path('itmusic/comment_like/playlist',views.com_like_list,name='com_like_list'),
    path('itmusic/delete_comment/song',views.com_delete_song,name='com_delete_song'),
    path('itmusic/delete_comment/album',views.com_delete_album,name='com_delete_album'),
    path('itmusic/delete_comment/playlist',views.com_delete_list,name='com_delete_list')
]

