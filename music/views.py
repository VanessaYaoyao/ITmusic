from django.shortcuts import render
from music.models import Album,AllLists,Song,User,TheList,Follow,Fan,LikeSongs,LikeAlbums,LikeLists,SongComment,SongReply,ListReply,ListComment,AlbumReply,AlbumComment,EmailVerifyRecord,SongCommentLike,AlbumCommentLike,ListCommentLike
from django.http import JsonResponse,HttpResponseRedirect
from django.db.models import Q
from django.forms.models import model_to_dict
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.
import json
import os
import random
from random import Random
import re
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField
from django.core.mail import send_mail
from web_project.settings import EMAIL_FROM
import simplejson
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160

def to_dict(obj, fields=None, exclude=None):
    data = {}
    for f in obj._meta.concrete_fields + obj._meta.many_to_many:
        value = f.value_from_object(obj)
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            value = [i.id for i in value] if obj.pk else None
        if isinstance(f, DateTimeField):
            value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
        data[f.name] = value
    return data
def index(request):
    return render(request,'index.html')

def top_songs(request):
    limit=request.GET.get('limit',10)
    t = request.GET.get('type','1')
    data={}
    try:
        limit = int(float(limit))
        data['count']=limit
        if t == '1':
            hit_songs = Song.objects.all().values()[:limit]
            for i in hit_songs:
                i['singer']=Album.objects.get(id=i['album_id']).singer
            data['hit_songs']=list(hit_songs)
            data['code']=200
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        if t == '2':
            new_songs = Song.objects.all().values().order_by('album__upload_time')[:limit]
            data['new_songs']=list(new_songs)
            for i in new_songs:
                i['singer']=Album.objects.get(id=i['album_id']).singer
            data['code'] = 200
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code']='404 NOT FOUND'
            data['errMsg']='NO results!'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results!'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def top_albums(request):
    limit=request.GET.get('limit',10)
    t = request.GET.get('type','1')
    data={}
    try:
        limit = int(float(limit))
        if t == '1':
            data['code']=200
            data['count'] = limit
            hit_albums = list(Album.objects.all().values())
            for i in hit_albums:
                songs = list(Song.objects.filter(album_id=i['id']).values())
                i['size']= len(songs)
                play_count = 0
                for j in songs:
                    play_count += j['play_count']
                i['play_count'] = play_count
                comment = AlbumComment.objects.filter(album_id=i['id'])
                comment_count = 0
                for j in comment:
                    comment_count += 1
                i['comment_count']=comment_count
            def myFunc(e):
                return e['play_count']
            hit_albums.sort(key=myFunc, reverse=True)
            data['hit_albums'] = hit_albums[:limit]
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        if t == '2':
            data['code'] = 200
            data['count'] = limit
            new_albums = Album.objects.all().values()[:limit]
            for i in new_albums:
                songs = list(Song.objects.filter(album_id=i['id']).values())
                i['size']=len(songs)
                play_count = 0
                for j in songs:
                    play_count += j['play_count']
                i['play_count'] = play_count
                comment = AlbumComment.objects.filter(album_id=i['id'])
                comment_count = 0
                for j in comment:
                    comment_count += 1
                i['comment_count'] = comment_count
            data['new_albums']=list(new_albums)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code']='404 NOT FOUND'
            data['errMsg']='NO results!'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results!'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def top_lists(request):
    limit=request.GET.get('limit',10)
    t = request.GET.get('type','1')
    data={}
    try:
        if t == '1':
            data['code']=200
            data['count'] = limit
            hit_lists = list(AllLists.objects.all().values())[:limit]
            for i in hit_lists:
                creator = to_dict(User.objects.get(id=i['user_id']), fields=['id', 'username'])
                i['creator']=creator
                comment = ListComment.objects.filter(the_list_id=i['id'])
                comment_count = 0
                for j in comment:
                    comment_count += 1
                i['comment_count']=comment_count
            data['hit_lists']=hit_lists
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        if t=='2':
            data['code'] = 200
            data['count'] = limit
            new_lists = list(
                AllLists.objects.all().values().order_by('-upload_time'))[:limit]
            for i in new_lists:
                creator = to_dict(User.objects.get(id=i['user_id']), fields=['id', 'username'])
                i['creator'] = creator
                comment = ListComment.objects.filter(the_list_id=i['id'])
                comment_count = 0
                for j in comment:
                    comment_count += 1
                i['comment_count'] = comment_count
            data['new_lists'] = new_lists
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND'
            data['errMsg'] = 'NO results!'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results!'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def random_str(randomlength=6):
    randomstr = ''
    chars = '0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        randomstr += chars[random.randint(0, length)]
    return randomstr

def send_email_code(email, send_type):
    code = random_str()
    email_record = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    send_title = ''
    send_body = ''
    # 如果为注册类型
    if send_type == "register":
        send_title = "注册验证码"
        send_body = "[ITmusic]您的注册验证码为：{0}".format(code)
        # 发送邮件
        send_mail(send_title, send_body, EMAIL_FROM, [email])
    if send_type == 'forget':
        send_title = "重置密码验证码"
        send_body = "[ITmusic]您的重置密码验证码为：{0}".format(code)
        # 发送邮件
        send_mail(send_title, send_body, EMAIL_FROM, [email])

def register(request):
    # session_key = request.session.session_key
    # request.session.delete(session_key)
    data={}
    if request.session.get('is_login', None):
        data['warning']='登录状态不允许注册。'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    req = simplejson.loads(request.body)
    username = req['username']
    password_1 = req['password1']
    password_2 = req['password2']
    email = req['email']
    for i in username:
        if i == '<' or i == '>' or i=='\n':
            username = username.replace(i, "")
    if email=="1164528260@qq.com":
        data['warning']='你已被列为网站黑名单！'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    if len(username) < 20 and len(password_1) < 15 and len(password_2) < 15 \
            and len(username) != 0 and len(password_1) != 0 and len(password_2) != 0 \
            and len(email) != 0 and len(email) < 30:
        if password_1 == password_2:
            judge1 = User.objects.filter(username=username)
            judge2 = User.objects.filter(email=email)
            if judge1.exists():
                data = {"warning": "该用户名已被占用。"}
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
                    if judge2.exists():
                        data = {"warning": "该邮箱已被占用。"}
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                    else:
                        send_email_code(email, 'register')
                        data = {'warning': "发送成功"}
                        data['code']=200
                        request.session['email'] = email
                        request.session['username'] = username
                        request.session['password'] = password_1
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data = {"warning": "邮箱格式不正确。"}
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data = {"warning": "两次密码不一致。"}
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        data = {"warning": "输入不能有过长或为空。"}
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def verify(request):
    data={}
    try:
        req = simplejson.loads(request.body)
        email_code=req['email_code']
        email = request.session.get('email')
        code_id = EmailVerifyRecord.objects.filter(email=email).values('id')
        code_id_list = []
        for i in code_id:
            code_id_list.append(i['id'])
        the_code = EmailVerifyRecord.objects.get(id=max(code_id_list))
        code = the_code.code
        if the_code.send_type=='register':
            username = request.session.get('username')
            password = request.session.get('password')
            if code == email_code:
                User.objects.create(username=username, email=email, password=password)
                session_key = request.session.session_key
                request.session.delete(session_key)
                data = {"warning": "通过验证，注册成功。"}
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data = {"warning": "验证码不正确"}
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            if code == email_code:
                data = {"warning": "通过验证，现在可重置密码"}
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data = {"warning": "验证码不正确"}
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='no results.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def findback(request):
    data={}
    try:
        req = simplejson.loads(request.body)
        email = req['email']
        email_check = User.objects.filter(email=email)
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            if email_check:
                send_email_code(email, 'forget')
                data = {"warning": "发送成功"}
                data['code']=200
                request.session['email'] = email
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data = {"warning": "该邮箱不存在。"}
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data = {"warning": "邮箱格式不正确。"}
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='No result'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def reset(request):
    email = request.session.get('email')
    data={}
    try:
        req = simplejson.loads(request.body)
        password1 = req['password1']
        password2 = req['password2']
        if 0 < len(password1) < 15 and 0 < len(password2) < 15:
            if password1 == password2:
                user = User.objects.get(email=email)
                user.password=password1
                user.save()
                session_key = request.session.session_key
                request.session.delete(session_key)
                data = {"warning": "密码重置成功。"}
                data['code'] = 200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data = {"warning": "两次密码不一致。"}
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data = {"warning": "新密码不可过长或为空。"}
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='No result'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def login(request):
    data={}
    req = simplejson.loads(request.body)
    username = req['username']
    password = req['password']
    try:
        user = User.objects.get(username=username)
        real_password=user.password
        if password==real_password:
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            data['message']='登陆成功'
            data['code'] = 200
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['errMsg']='密码或用户名错误！'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['errMsg']='用户名不存在！'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def logout(request):
    data={}
    if not request.session.get('is_login', None):
        data['warning']='您尚未登录！'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        request.session.flush()
        data['warning']='成功退出登录。'
        data['code'] = 200
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def check_song(request):
    id = request.GET.get('id', None)
    data = {}
    try:
        song = to_dict(Song.objects.get(id=id))
        song['song_url'] = str(song['song_url'])
        album = to_dict(Album.objects.get(id=song['album']))
        song['song_picture']=str(album['album_picture'])
        song['lyric']=str(song['lyric'])
        song['singer']=album['singer']
        song['album_name']=album['album_name']
        data['song'] = song
        like = list(LikeSongs.objects.filter(song_id=id))
        like_count = 0
        for i in like:
            like_count += 1
        data['song']['like_count'] = like_count
        comment = list(SongComment.objects.filter(song_id=id))
        comment_count = 0
        for i in comment:
            comment_count +=1
        data['song']['comment_count'] = comment_count
        user_id=request.session.get('user_id')
        if user_id:
            is_like = LikeSongs.objects.filter(user_id=user_id, song_id=id)
            if is_like:
                data['song']['is_like'] = True
            else:
                data['song']['is_like'] = False
        data['code']=200
        the_song = Song.objects.get(id=id)
        the_song.play_count+=1
        the_song.save()
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='No results'
        return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii':False})

def collect_song(request):
    data = {}
    try:
        if request.session.get('is_login', None):
            user_id = request.session.get('user_id')
            req=simplejson.loads(request.body)
            song_id = req['song_id']
            t = req['type']
            if song_id and t:
                if t == 1:
                    LikeSongs.objects.create(song_id=song_id,user_id=user_id)
                    data['warning'] = '收藏歌曲成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if t == 2:
                    LikeSongs.objects.filter(song_id=song_id,user_id=user_id).delete()
                    data['warning'] = '取消收藏成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['code'] = '404 NOT FOUND.'
                    data['errMsg'] = 'No result'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND.'
                data['errMsg'] = 'No result'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def song_comment(request):
    id = request.GET.get('id', None)
    data = {}
    try:#id有可能出错
        if request.method=='GET':#GET展示评论
            limit = request.GET.get('limit', 10)
            page = request.GET.get('page', 1)
            limit = int(float(limit))
            data['code']=200
            comments = SongComment.objects.filter(song_id=id).values('id','content','like_count','comment_time','sender_id')
            for i in comments:
                i['sender']=to_dict(User.objects.get(id=i['sender_id']),fields=['id','username','avatar'])
                i['sender']['avatar']=str(i['sender']['avatar'])
                user_id = request.session.get('user_id',None)
                if user_id:
                    is_like = SongCommentLike.objects.filter(user_id=user_id,comment_id=i['id'])
                    if is_like:
                        i['is_like']=True
                    else:
                        i['is_like']=False
            paginator = Paginator(comments, limit)
            try:
                comments = paginator.page(page)
            except (PageNotAnInteger, InvalidPage, EmptyPage):
                # 有错误, 返回第一页。
                comments = paginator.page(1)
            data['num_pages'] = comments.paginator.num_pages
            data['comments']=list(comments)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:#POST新增评论回复，或删除
            username = request.session.get('username')
            user_id = request.session.get('user_id')
            if username:
                req=simplejson.loads(request.body)
                content=req['content']
                song_id=req['song_id']
                if content:
                    if len(content)<=200:
                        n=1
                        for i in content:
                            if i == '\n':
                                n+=1
                            if i == '<' or i =='>':
                                content=content.replace(i,"")
                        if n>6:
                            content=content.replace("\n"," ")
                        SongComment.objects.create(content=content,sender_id=user_id,song_id=song_id)
                        data['message']='评论成功！'
                        data['code']=200
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                    else:
                        data['message'] = '评论长度过长！'
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['message']='评论内容不能为空！'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND'
                data['errMsg'] = 'Not logged in.'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results'
        return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii':False})

def check_album(request):
    id = request.GET.get('id', None)
    data = {}
    try:
        user_id = request.session.get('user_id')
        data['code']=200
        album = to_dict(Album.objects.get(id=id),exclude=['banner'])
        album['album_picture'] = str(album['album_picture'])
        songs = list(Song.objects.filter(album_id=id).values())
        play_count = 0
        for i in songs:
            play_count += i['play_count']
            if user_id:
                is_like = LikeSongs.objects.filter(user_id=user_id, song_id=i['id'])
                if is_like:
                    i['is_like'] = True
                else:
                    i['is_like'] = False
        data['album'] = album
        data['album']['songs'] = songs
        like = list(LikeAlbums.objects.filter(album_id=id))
        like_count = 0
        for i in like:
            like_count += 1
        data['album']['like_count'] = like_count
        comment = AlbumComment.objects.filter(album_id=id)
        comment_count = 0
        for i in comment:
            comment_count+=1
        data['album']['comment_count'] = comment_count
        data['album']['play_count']=play_count
        if user_id:
            is_like = LikeAlbums.objects.filter(user_id=user_id, album_id=id)
            if is_like:
                data['album']['is_like'] = True
            else:
                data['album']['is_like'] = False
        data['code']=200
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg'] = 'No result'
        return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii':False})
def collect_album(request):
    data = {}
    try:
        if request.session.get('is_login', None):
            user_id = request.session.get('user_id')
            req=simplejson.loads(request.body)
            album_id = req['album_id']
            t = req['type']
            if album_id and t:
                if t == 1:
                    LikeAlbums.objects.create(album_id=album_id,user_id=user_id)
                    data['warning'] = '收藏专辑成功！'
                    data['code']=200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if t == 2:
                    LikeAlbums.objects.filter(album_id=album_id,user_id=user_id).delete()
                    data['warning'] = '取消收藏成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['code'] = '404 NOT FOUND.'
                    data['errMsg'] = 'No result'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND.'
                data['errMsg'] = 'No result'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def album_comment(request):
    id = request.GET.get('id', None)
    data = {}
    try:
        if request.method=="GET":
            limit = request.GET.get('limit', 10)
            page = request.GET.get('page', 1)
            limit = int(float(limit))
            data['code']=200
            comments = list(AlbumComment.objects.filter(album_id=id).values('id','content','like_count','comment_time','sender_id'))
            for i in comments:
                i['sender']=to_dict(User.objects.get(id=i['sender_id']),fields=['id','username','avatar'])
                i['sender']['avatar']=str(i['sender']['avatar'])
                user_id = request.session.get('user_id',None)
                if user_id:
                    is_like = AlbumCommentLike.objects.filter(user_id=user_id,comment_id=i['id'])
                    if is_like:
                        i['is_like']=True
                    else:
                        i['is_like']=False
            paginator = Paginator(comments, limit)
            try:
                comments = paginator.page(page)
            except (PageNotAnInteger, InvalidPage, EmptyPage):
                # 有错误, 返回第一页。
                comments = paginator.page(1)
            data['num_pages'] = comments.paginator.num_pages
            data['comments']=list(comments)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            username = request.session.get('username')
            user_id=request.session.get('user_id')
            if username:
                req = simplejson.loads(request.body)
                content = req['content']
                album_id = req['album_id']
                if content:
                    AlbumComment.objects.create(content=content, sender_id=user_id, album_id=album_id)
                    data['message'] = '评论成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['message'] = '评论内容不能为空'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND'
                data['errMsg'] = 'Not logged in.'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='NO results'
        return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii':False})
def check_list(request):
    id = request.GET.get('id', None)
    data = {}
    try:
        user_id=request.session.get('user_id')
        list_info = to_dict(AllLists.objects.get(id=id),exclude=['user'])
        creator_id = to_dict(AllLists.objects.get(id=id),fields=['user'])
        creator = to_dict(User.objects.get(id=creator_id['user']),fields=['id','username'])
        list_info['list_picture']=str(list_info['list_picture'])
        songs = TheList.objects.filter(all_lists_id=list_info['id']).values('song_id')
        songs=list(songs)
        for i in songs:
            i['song_name']=Song.objects.get(id=i['song_id']).song_name
            i['album']=Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).album_name
            i['singer']=Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).singer
            if user_id:
                is_like = LikeSongs.objects.filter(user_id=user_id, song_id=i['song_id'])
                if is_like:
                    i['is_like'] = True
                else:
                    i['is_like'] = False
        data['list']=list_info
        data['list']['creator']=creator
        data['list']['songs']=songs
        like = list(LikeLists.objects.filter(list_id=id))
        like_count = 0
        for i in like:
            like_count += 1
        data['list']['like_count'] = like_count
        comment = list(ListComment.objects.filter(the_list_id=id))
        comment_count = 0
        for i in comment:
            comment_count+=1
        data['list']['comment_count'] = comment_count
        data['code'] = 200
        if user_id:
            is_like = LikeLists.objects.filter(user_id=user_id, list_id=id)
            if is_like:
                data['list']['is_like'] = True
            else:
                data['list']['is_like'] = False
        the_list=AllLists.objects.get(id=id)
        the_list.play_count+=1
        the_list.save()
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='NO result'
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def collect_playlist(request):
    data = {}
    try:
        if request.session.get('is_login', None):
            user_id = request.session.get('user_id')
            req=simplejson.loads(request.body)
            list_id = req['list_id']
            t = req['type']
            if list_id and t:
                if t == 1:
                    LikeLists.objects.create(list_id=list_id,user_id=user_id)
                    data['warning'] = '收藏歌单成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if t == 2:
                    LikeLists.objects.filter(list_id=list_id,user_id=user_id).delete()
                    data['warning'] = '取消收藏成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['code'] = '404 NOT FOUND.'
                    data['errMsg'] = 'No result'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND.'
                data['errMsg'] = 'No result'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def list_comment(request):
    id = request.GET.get('id', None)
    data = {}
    try:
        if request.method=='GET':
            limit = request.GET.get('limit', 10)
            page = request.GET.get('page', 1)
            limit = int(float(limit))
            data['code'] = 200
            comments = list(ListComment.objects.filter(the_list_id=id).values('id', 'content', 'like_count', 'comment_time', 'sender_id'))
            for i in comments:
                i['sender'] = to_dict(User.objects.get(id=i['sender_id']), fields=['id', 'username', 'avatar'])
                i['sender']['avatar'] = str(i['sender']['avatar'])
                user_id = request.session.get('user_id',None)
                if user_id:
                    is_like = ListCommentLike.objects.filter(user_id=user_id,comment_id=i['id'])
                    if is_like:
                        i['is_like']=True
                    else:
                        i['is_like']=False
            paginator = Paginator(comments, limit)
            try:
                comments = paginator.page(page)
            except (PageNotAnInteger, InvalidPage, EmptyPage):
                # 有错误, 返回第一页。
                comments = paginator.page(1)
            data['num_pages'] = comments.paginator.num_pages
            data['comments'] = list(comments)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            username = request.session.get('username')
            user_id = request.session.get('user_id')
            if username:
                req = simplejson.loads(request.body)
                content = req['content']
                list_id = req['list_id']
                if content:
                    ListComment.objects.create(content=content, sender_id=user_id, the_list_id=list_id)
                    data['message'] = '评论成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['message'] = '评论内容不能为空'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND'
                data['errMsg'] = 'Not logged in.'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def search(request):
    data = {}
    try:
        sc = request.GET.get('keywords',None)
        t = request.GET.get('type','1')
        limit = request.GET.get('limit',30)
        search_album = []
        search_user = []
        search_song = []
        search_list = []
        if sc:
            search_album = Album.objects.filter(Q(album_name__icontains=sc)).values()[:limit]
            search_user = User.objects.filter(Q(username__icontains=sc)).values('id','username','avatar')[:limit]
            search_list = AllLists.objects.filter(Q(list_name__icontains=sc)).values()[:limit]
            for i in search_list:
                i['creator']=to_dict(User.objects.get(id=i['user_id']),fields=['id','username'])
            search_song = Song.objects.filter(Q(song_name__icontains=sc)).values()[:limit]
        search_song = list(search_song)
        for i in search_song:
            i['singer'] = Album.objects.get(id=i['album_id']).singer
            i['album_name'] = Album.objects.get(id=i['album_id']).album_name
        data['code'] = 200

        if t == '1':
            data['search_song']=search_song
            return JsonResponse(data,safe=False,json_dumps_params={'ensure_ascii':False})
        if t == '2':
            data['search_album']=list(search_album)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        if t == '3':
            data['search_list']=list(search_list)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        if t == '4':
            data['search_user']=list(search_user)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND'
            data['errMsg'] = 'No results'
            return JsonResponse(data)
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'No results'
        return JsonResponse(data)
def account(request):
    data = {}
    try:
        id=request.session.get('user_id')
        user = to_dict(User.objects.get(id=id), exclude=['password'])
        user['avatar'] = str(user['avatar'])
        data['user'] = user

        follows = Follow.objects.filter(user_id=id).values('follow_id')
        follows = list(follows)
        for i in follows:
            i['username'] = User.objects.get(id=i['follow_id']).username
            i['avatar'] = str(User.objects.get(id=i['follow_id']).avatar)
        data['follows']=follows
        fans = Fan.objects.filter(user_id=id).values('fan_id')
        fans = list(fans)
        for i in fans:
            i['username'] = User.objects.get(id=i['fan_id']).username
            i['avatar'] = str(User.objects.get(id=i['fan_id']).avatar)
        data['fans']=fans

        create_lists = AllLists.objects.filter(user_id=id).values()
        for i in create_lists:
            songs = list(TheList.objects.filter(all_lists_id=i['id']).values('song_id'))
            for j in songs:
                j['song_name']=Song.objects.get(id=j['song_id']).song_name
                j['song_picture'] = str(Album.objects.get(id=Song.objects.get(id=j['song_id']).album_id).album_picture)
                j['singer'] = Album.objects.get(id=Song.objects.get(id=j['song_id']).album_id).singer
            i['song']=songs
            like = list(LikeLists.objects.filter(list_id=i['id']))
            like_count = 0
            for j in like:
                like_count += 1
            comment = ListComment.objects.filter(the_list_id=i['id'])
            comment_count = 0
            for j in comment:
                comment_count += 1
            i['like_count'] = like_count
            i['comment_count'] = comment_count
        data['count'] = len(list(create_lists))
        # for i in create_lists:
        #     songs=list(TheList.objects.filter(all_lists_id=i['id']).values('song_id'))
        #     for j in songs:
        #         j['song_name']=Song.objects.get(id=j['song_id']).song_name
        #         j['song_picture'] = str(Album.objects.get(id=Song.objects.get(id=j['song_id']).album_id).album_picture)
        #         j['singer'] = Album.objects.get(id=Song.objects.get(id=j['song_id']).album_id).singer
        #     i['song']=songs

        data['create_lists']= list(create_lists)

        like_songs = LikeSongs.objects.filter(user_id=id).values('song_id')
        like_songs = list(like_songs)
        data['count'] = len(like_songs)
        for i in like_songs:
            i['song_name'] = Song.objects.get(id=i['song_id']).song_name
            i['play_count'] = Song.objects.get(id=i['song_id']).play_count
            comment = list(SongComment.objects.filter(song_id=i['song_id']))
            comment_count = 0
            for j in comment:
                comment_count += 1
            like = list(LikeSongs.objects.filter(song_id=i['song_id']))
            like_count = 0
            for j in like:
                like_count += 1
            i['comment_count'] = comment_count
            i['like_count'] = like_count
            i['singer'] = Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).singer
            i['upload_time'] = Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).upload_time
            album = to_dict(Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id),
                            fields=['id', 'album_name'])
            i['album'] = album
            i['song_picture'] = str(
                to_dict(Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id), fields=['album_picture'])[
                    'album_picture'])
        # for i in like_songs:
        #     i['song_name'] = Song.objects.get(id=i['song_id']).song_name
        #     i['singer'] = Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).singer
        #     i['song_picture'] = Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).album_picture
        data['like_songs']=like_songs

        # like_albums = LikeAlbums.objects.filter(user_id=id).values('album_id')
        # like_albums = list(like_albums)
        # for i in like_albums:
        #     i['album_name'] = Album.objects.get(id=i['album_id']).album_name
        #     i['singer'] = Album.objects.get(id=i['album_id']).singer
        #     i['album_picture'] = str(Album.objects.get(id=i['album_id']).album_picture)
        like_albums = LikeAlbums.objects.filter(user_id=id).values('album_id')
        like_albums = list(like_albums)
        data['count'] = len(like_albums)
        for i in like_albums:
            i['album_name'] = Album.objects.get(id=i['album_id']).album_name
            i['singer'] = Album.objects.get(id=i['album_id']).singer
            i['description'] = Album.objects.get(id=i['album_id']).description
            i['upload_time'] = Album.objects.get(id=i['album_id']).upload_time
            i['album_picture'] = str(Album.objects.get(id=i['album_id']).album_picture)
            like = list(LikeAlbums.objects.filter(album_id=i['album_id']))
            like_count = 0
            for j in like:
                like_count += 1
            comment = AlbumComment.objects.filter(album_id=i['album_id'])
            comment_count = 0
            for j in comment:
                comment_count += 1
            i['like_count'] = like_count
            i['comment_count'] = comment_count
        data['like_albums']=like_albums

        like_lists = LikeLists.objects.filter(user_id=id).values('list_id')
        like_lists = list(like_lists)
        data['count'] = len(like_lists)
        for i in like_lists:
            i['list_name'] = AllLists.objects.get(id=i['list_id']).list_name
            i['creator_id'] = AllLists.objects.get(id=i['list_id']).user_id
            i['creator_username'] = User.objects.get(id=i['creator_id']).username
            i['description'] = AllLists.objects.get(id=i['list_id']).description
            i['upload_time'] = AllLists.objects.get(id=i['list_id']).upload_time
            i['list_picture'] = str(AllLists.objects.get(id=i['list_id']).list_picture)
            like = list(LikeLists.objects.filter(list_id=i['list_id']))
            like_count = 0
            for j in like:
                like_count += 1
            comment = ListComment.objects.filter(the_list_id=i['list_id'])
            comment_count = 0
            for j in comment:
                comment_count += 1
            i['like_count'] = like_count
            i['comment_count'] = comment_count
        # for i in like_lists:
        #     i['list_name']=AllLists.objects.get(id=i['list_id']).list_name
        #     i['creator_id']=AllLists.objects.get(id=i['list_id']).user_id
        #     i['creator_username']=User.objects.get(id=i['creator_id']).username
        #     songs=list(TheList.objects.filter(all_lists_id=i['list_id']).values('song_id'))
        #     for j in songs:
        #         j['song_name']=Song.objects.get(id=j['song_id']).song_name
        #         j['singer'] = Album.objects.get(id=Song.objects.get(id=j['song_id']).album_id).singer
        #         j['song_picture'] = Album.objects.get(id=Song.objects.get(id=j['song_id']).album_id).album_picture
        #     i['song']=songs
        data['like_lists']=like_lists
        data['code']=200
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code']='404 NOT FOUND'
        data['errMsg']='Not logged in.'
        return JsonResponse(data)
def userinfo(request):
    data={}
    if request.session.get('is_login', None):
        id=request.session.get('user_id')
        if request.method=='GET':
            data['user']=to_dict(User.objects.get(id=id))
            data['user']['avatar']=str(data['user']['avatar'])
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            avatar=request.FILES.get('avatar',"")
            description = request.POST.get('description',"")
            address = request.POST.get('address',"")
            gender = request.POST.get('gender',"")
            age = request.POST.get('age',0)
            username = request.POST.get('username')
            if username:
                user_id = request.session.get('user_id')
                user = User.objects.get(id=user_id)
                if username != user.username:
                    same_username = User.objects.filter(username=username)
                    if same_username:
                        data['message']='该用户名已被占用！'
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                    if len(username)>20:
                        data['message']='用户名过长！'
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

                user.username=username
                user.age=age
                if age<=120 and age>=0:
                    user.age = age
                else:
                    data['message'] = '年龄不合规范！'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                user.gender=gender
                user.description=description
                user.address=address
                if len(description)<=200:
                    n=0
                    for i in description:
                        if i == '\n':
                            n += 1
                        if i == '<' or i == '>':
                            description = description.replace(i, "")
                    if n > 6:
                        description = description.replace("\n", " ")
                    user.description=description
                else:
                    data['message'] = '简介过长！'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if len(address)<=50:
                    user.address = address
                else:
                    data['message'] = '地址过长！'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if avatar:
                    type_list = ['.jpg', '.png', '.gif', '.webp']
                    if os.path.splitext(avatar.name)[1].lower() in type_list:
                        if avatar.size > 10485760:
                            data['message']='头像大小不可超过10！'
                            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                        else:
                            user.avatar=avatar
                    else:
                        data['message']='头像格式不正确！'
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                user.save()
                data['message']='修改成功！'
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['message']='用户名不能为空！'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not logged in'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def follow(request):
    data={}
    try:
        if request.session.get('is_login',None):
            user_id=request.session.get('user_id')
            req=simplejson.loads(request.body)
            follow_id = req['user_id']
            t = req['type']
            if follow_id and t:
                the_follow = User.objects.get(id=follow_id)
                the_user = User.objects.get(id=user_id)
                if t== 1:
                    Follow.objects.create(user_id=user_id,follow_id=follow_id)
                    Fan.objects.create(user_id=follow_id,fan_id=user_id)
                    the_follow.fan_count +=1
                    the_follow.save()
                    the_user.follow_count +=1
                    the_user.save()
                    data['warning']='关注成功！'
                    data['code']=200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if t==2:
                    delete_follow = Follow.objects.filter(user_id=user_id,follow_id=follow_id)
                    delete_follow.delete()
                    delete_fan = Fan.objects.filter(user_id=follow_id,fan_id=user_id)
                    delete_fan.delete()
                    the_follow.fan_count -= 1
                    the_follow.save()
                    the_follow.save()
                    the_user.follow_count -= 1
                    the_user.save()
                    data['warning'] = '取消关注成功！'
                    data['code'] = 200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['code'] = '404 NOT FOUND.'
                    data['errMsg'] = 'No result'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['code'] = '404 NOT FOUND.'
                data['errMsg'] = 'No result'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'No result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def check_user(request):
    id = request.GET.get('id', None)
    data = {}
    try:
        user = to_dict(User.objects.get(id=id),exclude=['password'])
        user['avatar']=str(user['avatar'])
        data['user']=user

        follows = Follow.objects.filter(user_id=id).values('follow_id')
        follows = list(follows)
        for i in follows:
            i['username']=User.objects.get(id=i['follow_id']).username
            i['avatar']=str(User.objects.get(id=i['follow_id']).avatar)
        fans = Fan.objects.filter(user_id=id).values('fan_id')
        fans = list(fans)
        for i in fans:
            i['username'] = User.objects.get(id=i['fan_id']).username
            i['avatar'] = str(User.objects.get(id=i['fan_id']).avatar)
        user_id = request.session.get('user_id', None)
        if user_id:
            is_follow = Follow.objects.filter(user_id=user_id, follow_id=id)
            if is_follow:
                data['is_follow'] = True
            else:
                data['is_follow'] = False

        data['follows']=follows
        data['fans'] = fans
        data['code']=200
    except:
        data['code']= '404 NOT FOUND'
        data['errMsg']='No results'

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def user_songs(request):
    id = request.GET.get('id', None)
    limit = request.GET.get('limit',10)
    page = request.GET.get('page',1)
    data = {}
    try:
        limit=int(float(limit))
        like_songs = LikeSongs.objects.filter(user_id=id).values('song_id')
        like_songs = list(like_songs)
        data['count']=len(like_songs)
        for i in like_songs:
            i['song_name'] = Song.objects.get(id=i['song_id']).song_name
            i['play_count'] = Song.objects.get(id=i['song_id']).play_count
            comment = list(SongComment.objects.filter(song_id=i['song_id']))
            comment_count = 0
            for j in comment:
                comment_count += 1
            like = list(LikeSongs.objects.filter(song_id=i['song_id']))
            like_count = 0
            for j in like:
                like_count += 1
            i['comment_count']=comment_count
            i['like_count'] = like_count
            i['singer'] = Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).singer
            i['upload_time']= Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id).upload_time
            album=to_dict(Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id),fields=['id','album_name'])
            i['album']=album
            i['song_picture']=str(to_dict(Album.objects.get(id=Song.objects.get(id=i['song_id']).album_id),fields=['album_picture'])['album_picture'])
        paginator = Paginator(like_songs, limit)
        try:
            like_songs = paginator.page(page)
        except (PageNotAnInteger, InvalidPage, EmptyPage):
            # 有错误, 返回第一页。
            like_songs = paginator.page(1)
        data['like_songs'] = list(like_songs)
        data['code']=200
        data['num_pages']=like_songs.paginator.num_pages
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results!'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def user_albums(request):
    id = request.GET.get('id', None)
    limit = request.GET.get('limit',10)
    page = request.GET.get('page',1)
    data={}
    try:
        like_albums = LikeAlbums.objects.filter(user_id=id).values('album_id')
        like_albums = list(like_albums)
        data['count']=len(like_albums)
        for i in like_albums:
            i['album_name'] = Album.objects.get(id=i['album_id']).album_name
            i['singer'] = Album.objects.get(id=i['album_id']).singer
            i['description']=Album.objects.get(id=i['album_id']).description
            i['upload_time']=Album.objects.get(id=i['album_id']).upload_time
            i['album_picture'] = str(Album.objects.get(id=i['album_id']).album_picture)
            like = list(LikeAlbums.objects.filter(album_id=i['album_id']))
            like_count = 0
            for j in like:
                like_count += 1
            comment = AlbumComment.objects.filter(album_id=i['album_id'])
            comment_count = 0
            for j in comment:
                comment_count += 1
            i['like_count'] = like_count
            i['comment_count'] = comment_count
        paginator = Paginator(like_albums, limit)
        try:
            like_albums = paginator.page(page)
        except (PageNotAnInteger, InvalidPage, EmptyPage):
            # 有错误, 返回第一页。
            like_albums = paginator.page(1)
        data['like_albums']=list(like_albums)
        data['num_pages'] = like_albums.paginator.num_pages
        data['code']=200
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results!'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def user_lists(request):
    id = request.GET.get('id', None)
    t = request.GET.get('type', '1')
    limit = request.GET.get('limit',10)
    page = request.GET.get('page',1)
    data={}
    try:
        if t == '1':
            like_lists = LikeLists.objects.filter(user_id=id).values('list_id')
            like_lists = list(like_lists)
            data['count']=len(like_lists)
            for i in like_lists:
                i['list_name']=AllLists.objects.get(id=i['list_id']).list_name
                i['creator_id']=AllLists.objects.get(id=i['list_id']).user_id
                i['creator_username']=User.objects.get(id=i['creator_id']).username
                i['description'] = AllLists.objects.get(id=i['list_id']).description
                i['upload_time'] = AllLists.objects.get(id=i['list_id']).upload_time
                i['list_picture']=str(AllLists.objects.get(id=i['list_id']).list_picture)
                like = list(LikeLists.objects.filter(list_id=i['list_id']))
                like_count = 0
                for j in like:
                    like_count += 1
                comment = ListComment.objects.filter(the_list_id=i['list_id'])
                comment_count = 0
                for j in comment:
                    comment_count += 1
                i['like_count'] = like_count
                i['comment_count'] = comment_count
            paginator = Paginator(like_lists, limit)
            try:
                like_lists = paginator.page(page)
            except (PageNotAnInteger, InvalidPage, EmptyPage):
                # 有错误, 返回第一页。
                like_lists = paginator.page(1)
            data['like_lists']=list(like_lists)
            data['num_pages'] = like_lists.paginator.num_pages
            data['code']=200
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        if t == '2':
            create_lists =list(AllLists.objects.filter(user_id=id).values())
            for i in create_lists:
                like = list(LikeLists.objects.filter(list_id=i['id']))
                like_count = 0
                for j in like:
                    like_count += 1
                comment = ListComment.objects.filter(the_list_id=i['id'])
                comment_count = 0
                for j in comment:
                    comment_count += 1
                i['like_count'] = like_count
                i['comment_count'] = comment_count
            data['count']=len(list(create_lists))
            paginator = Paginator(create_lists, limit)
            try:
                create_lists = paginator.page(page)
            except (PageNotAnInteger, InvalidPage, EmptyPage):
                # 有错误, 返回第一页。
                create_lists = paginator.page(1)
            data['create_lists']= list(create_lists)
            data['num_pages'] = create_lists.paginator.num_pages
            data['code'] = 200
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND'
        data['errMsg'] = 'NO results!'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def banner(request):
    data={}
    banners = list(Album.objects.all().values('banner','id','album_name'))
    for i in banners:
        songs = list(Song.objects.filter(album_id=i['id']).values())
        play_count = 0
        for j in songs:
            play_count += j['play_count']
        i['play_count']=play_count

    def myFunc(e):
        return e['play_count']
    banners.sort(key=myFunc,reverse=True)
    data['hit_albums']=banners[:5]
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def change_password(request):
    data = {}
    username = request.session.get('username',None)
    if username:
        user=User.objects.get(username=username)
        real_password=user.password
        req = simplejson.loads(request.body)
        old_password=req['old_password']
        password1 = req['password1']
        password2 = req['password2']
        if old_password == '' or password1 == '' or password2 == '':
            data['message'] = '填写内容不能为空！'
        else:
            if password2 !=password1:
                data['message'] = '两次密码不相同！'
            else:
                if len(password1) < 4 or len(password1)>30:
                    data['message'] = '密码长度不符合规范！'
                else:
                    import string
                    s = string.digits + string.ascii_letters + string.punctuation
                    for i in password1:
                        if i not in s:
                            data['message'] = '密码中有不符合规范的字符！'
                    else:
                        if old_password != real_password:
                            data['message'] = '旧密码填写错误！'
                        else:
                            user.password = password1
                            user.save()
                            data['message'] = '修改成功！'
                            data['code']=200
    else:
        data['code']='404 NOT FOUND'
        data['errMsg']='Not logged in.'
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def addin_playlist(request):
    data={}
    try:
        user_id=request.session.get('user_id',None)
        if user_id:
            if request.method=="GET":
                create_lists=list(AllLists.objects.filter(user_id=user_id).values('id','list_name'))
                data['create_lists']=create_lists
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                req=simplejson.loads(request.body)
                song_id=req['song_id']
                list_id=req['list_id']
                t = req['type']
                if t == 1:
                    TheList.objects.create(all_lists_id=list_id,song_id=song_id)
                    data['message']='加入成功！'
                    data['code']=200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                if t == 2:
                    TheList.objects.filter(all_lists_id=list_id,song_id=song_id).delete()
                    data['message'] = '取消加入成功！'
                    data['code']=200
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['errMsg']='Not logged in.'
            data['code']='404 NOT FOUND.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['errMsg'] = 'No result.'
        data['code'] = '404 NOT FOUND.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def create_list(request):
    data={}
    user_id= request.session.get('user_id',None)
    if user_id:
        list_name = request.POST.get('list_name')
        for i in list_name:
            if i == '<' or i == '>' or i=='\n':
                list_name = list_name.replace(i, "")
        list_picture = request.FILES.get('list_picture',"")
        description= request.POST.get('list_description',"")
        n = 0
        for i in description:
            if i == '\n':
                n += 1
            if i == '<' or i == '>':
                description = description.replace(i, "")
        if n > 6:
            description = description.replace("\n", " ")
        if list_name:
            if list_picture:
                type_list = ['.jpg', '.png', '.gif', '.webp']
                if os.path.splitext(list_picture.name)[1].lower() in type_list:
                    if list_picture.size>10485760:
                        data['message']='图片大小不得超过10M!'
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                    else:
                        AllLists.objects.create(list_name=list_name, list_picture=list_picture, description=description,
                                                user_id=user_id)
                        data['message'] = '创建成功'
                        data['code']=200
                        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
                else:
                    data['message'] = '图片格式不正确！'
                    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                AllLists.objects.create(list_name=list_name,list_picture=list_picture,description=description,user_id=user_id)
                data['message']='创建成功'
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['message']='歌单名不能为空！'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        data['errMsg'] = 'Not logged in.'
        data['code'] = '404 NOT FOUND.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def delete_list(request):
    data={}
    try:
        user_id=request.session.get('user_id',None)
        if user_id:
            req=simplejson.loads(request.body)
            list_id=req['list_id']
            the_list = AllLists.objects.get(id=list_id)
            if the_list.user_id==user_id:
                the_list.delete()
                data['message']='删除成功！'
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['message']='您不是该歌单的创建者！'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'No result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def com_like_song(request):
    data={}
    user_id = request.session.get('user_id',None)
    if user_id:
        try:
            req=simplejson.loads(request.body)
            comment_id = req['comment_id']
            t = req['type']
            the_comment = SongComment.objects.get(id=comment_id)
            if t==1:
                the_comment.like_count+=1
                the_comment.save()
                SongCommentLike.objects.create(comment_id=comment_id,user_id=user_id)
                data['message']='点赞成功！'
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            if t==2:
                the_comment.like_count -= 1
                the_comment.save()
                SongCommentLike.objects.filter(comment_id=comment_id,user_id=user_id).delete()
                data['message'] = '取消点赞成功！'
                data['code'] = 200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        except:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'No result.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not logged in.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def com_like_album(request):
    data={}
    user_id = request.session.get('user_id',None)
    if user_id:
        try:
            req=simplejson.loads(request.body)
            comment_id = req['comment_id']
            t = req['type']
            the_comment = AlbumComment.objects.get(id=comment_id)
            if t==1:
                the_comment.like_count+=1
                the_comment.save()
                AlbumCommentLike.objects.create(comment_id=comment_id,user_id=user_id)
                data['message']='点赞成功！'
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            if t==2:
                the_comment.like_count -= 1
                the_comment.save()
                AlbumCommentLike.objects.filter(comment_id=comment_id,user_id=user_id).delete()
                data['message'] = '取消点赞成功！'
                data['code'] = 200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        except:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'No result.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not logged in.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def com_like_list(request):
    data={}
    user_id = request.session.get('user_id',None)
    if user_id:
        try:
            req=simplejson.loads(request.body)
            comment_id = req['comment_id']
            t = req['type']
            the_comment = ListComment.objects.get(id=comment_id)
            if t==1:
                the_comment.like_count+=1
                the_comment.save()
                ListCommentLike.objects.create(comment_id=comment_id,user_id=user_id)
                data['message']='点赞成功！'
                data['code']=200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            if t==2:
                the_comment.like_count -= 1
                the_comment.save()
                ListCommentLike.objects.filter(comment_id=comment_id,user_id=user_id).delete()
                data['message'] = '取消点赞成功！'
                data['code'] = 200
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        except:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'No result.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'Not logged in.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def com_delete_song(request):
    data={}
    req=simplejson.loads(request.body)
    comment_id = req['comment_id']
    try:
        username=request.session.get('username',None)
        user_id = request.session.get('user_id')
        if username:
            the_comment = SongComment.objects.get(id=comment_id)
            if the_comment.sender_id==user_id:
                the_comment.delete()
                data['code']=200
                data['message']='删除成功！'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['message']='Not sender.'
                data['code']='404 NOT FOUND.'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'No result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def com_delete_album(request):
    data={}
    req=simplejson.loads(request.body)
    comment_id = req['comment_id']
    try:
        username=request.session.get('username',None)
        user_id = request.session.get('user_id')
        if username:
            the_comment = AlbumComment.objects.get(id=comment_id)
            if the_comment.sender_id==user_id:
                the_comment.delete()
                data['code']=200
                data['message']='删除成功！'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['message']='Not sender.'
                data['code']='404 NOT FOUND.'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'No result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
def com_delete_list(request):
    data={}
    req=simplejson.loads(request.body)
    comment_id = req['comment_id']
    try:
        username=request.session.get('username',None)
        user_id = request.session.get('user_id')
        if username:
            the_comment = ListComment.objects.get(id=comment_id)
            if the_comment.sender_id==user_id:
                the_comment.delete()
                data['code']=200
                data['message']='删除成功！'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                data['message']='Not sender.'
                data['code']='404 NOT FOUND.'
                return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            data['code'] = '404 NOT FOUND.'
            data['errMsg'] = 'Not logged in.'
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    except:
        data['code'] = '404 NOT FOUND.'
        data['errMsg'] = 'No result.'
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})