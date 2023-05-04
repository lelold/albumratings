from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


from math import ceil

from .models import Artist, Album, Rating


def search_album(request, search_req):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    albums = Album.objects.filter(name__icontains=search_req)
    return render(request, 'albums/search_album.html', {
        'albums': albums,
        'search_req': search_req,
        'auth': auth,
        'username': username,
        'user': user,
    })


def search_artist(request, search_req):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    artists = Artist.objects.filter(name__icontains=search_req)
    return render(request, 'albums/search_artist.html', {
        'artists': artists,
        'search_req': search_req,
        'auth': auth,
        'username': username,
        'user': user,
    })


def search_user(request, search_req):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    users = User.objects.filter(username__icontains=search_req)
    return render(request, 'albums/search_user.html', {
        'search_req': search_req,
        'auth': auth,
        'username': username,
        'user': user,
        'users': users,
    })


def search(request, search_req):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    albums = Album.objects.filter(name__icontains=search_req)[:3]
    artists = Artist.objects.filter(name__icontains=search_req)[:3]
    users = User.objects.filter(username__icontains=search_req)[:3]
    return render(request, 'albums/search.html', {
        'albums': albums,
        'artists': artists,
        'search_req': search_req,
        'auth': auth,
        'username': username,
        'user': user,
        'users': users,
    })


def index(request):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    if request.method == 'POST':
        search_req = request.POST['search']
        if search_req:
            return search(request, search_req)
        else:
            albums_list = Album.objects.all()[:4]
            return render(request, 'albums/index.html', {
                'albums_list': albums_list,
                'auth': auth,
                'username': username,
                'user': user,
            })
    albums_list = Album.objects.all()[:4]
    return render(request, 'albums/index.html', {
        'albums_list': albums_list,
        'auth': auth,
        'username': username,
        'user': user,
    })


def vote(request, album_id):
    if request.user.is_authenticated:
        album = get_object_or_404(Album, pk=album_id)
        try:
            if request.POST['i'] == '0':
                try:
                    old_rate = Rating.objects.get(user=request.user, album=album)
                    album.rating_all -= int(old_rate.num)
                    album.rating_num -= 1
                    old_rate.delete()
                    album.rating = round((album.rating_all / 1.0) / (album.rating_num / 1.0), 2)
                    album.save()
                except Rating.DoesNotExist:
                    pass
            else:
                if Rating.objects.filter(user=request.user, album=album, num=request.POST['i']).exists():
                    pass
                elif Rating.objects.filter(user=request.user, album=album).exists():
                    old_rate = Rating.objects.get(user=request.user, album=album)
                    album.rating_all -= int(old_rate.num)
                    old_rate.delete()
                    new_rate = Rating(user=request.user, album=album, num=request.POST['i'])
                    new_rate.save()
                    album.rating_all += int(new_rate.num)
                    album.rating = round((album.rating_all / 1.0) / (album.rating_num / 1.0), 2)
                    album.save()
                else:
                    rate = Rating(album=album, user=request.user, num=request.POST['i'])
                    rate.save()
                    album.rating_num += 1
                    album.rating_all += int(rate.num)
                    album.rating = round((album.rating_all / 1.0) / (album.rating_num / 1.0), 2)
                    album.save()
        except MultiValueDictKeyError:
            pass
    else:
        raise AssertionError('You are not logged into your account')


def detail(request, album_id):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
        if Rating.objects.filter(user=user, album=get_object_or_404(Album, pk=album_id)).exists():
            rating_num = Rating.objects.get(user=user, album=get_object_or_404(Album, pk=album_id)).num
            rated = True
        else:
            rating_num = ''
            rated = False
    else:
        auth = False
        username = ''
        user = ''
        rating_num = ''
        rated = False
    error = ''
    album = get_object_or_404(Album, pk=album_id)
    l = list(range(1, 11))
    if request.method == 'POST':
        try:
            vote(request, album_id)
        except AssertionError as err:
            error = str(err)
    return render(request, 'albums/detail.html', {
        'album': album,
        'l': l,
        'error': error,
        'auth': auth,
        'username': username,
        'user': user,
        'rating_num': rating_num,
        'rated': rated,
    })


def page(request, page_id):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    if request.method == 'POST':
        search_req = request.POST['search']
        return search(request, search_req)
    page_all = ceil(len(Album.objects.all()) / 4)
    page_ids = [i for i in range(1, page_all + 1)]
    albums_on_page = list(Album.objects.all())[page_id * 4 - 4:page_id * 4]
    next_page = page_id + 1
    if page_id > 0:
        prev_page = page_id - 1
    else:
        prev_page = False
    return render(request, 'albums/page.html', {
        'albums': albums_on_page,
        'page_ids': page_ids,
        'next_page': next_page,
        'prev_page': prev_page,
        'auth': auth,
        'username': username,
        'user': user,
    })


def detail_artist(request, artist_id):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    artist = get_object_or_404(Artist, pk=artist_id)
    albums_list = [i for i in Album.objects.order_by('release_year') if i.artist == artist]
    max_rating = albums_list[0].rating
    best_album = albums_list[0]
    for i in albums_list:
        if i.rating > max_rating:
            max_rating = i.rating
            best_album = i
    return render(request, 'albums/artist.html', {
        'artist': artist,
        'best_album': best_album,
        'album_list': albums_list,
        'auth': auth,
        'username': username,
        'user': user,
    })


def registration(request):
    if request.method == 'POST':
        try:
            register(request, request.POST['username'], request.POST['email'], request.POST['password'], request.POST['r_password'])
        except AssertionError as err:
            error = str(err)
            return render(request, 'albums/registration.html', {
                'error': error
            })
        else:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.save()
                return HttpResponseRedirect(reverse('albums:login'))
            except IntegrityError:
                error = 'Oops, this user is already exists!'
                return render(request, 'albums/registration.html', {
                    'error': error
                })
    return render(request, 'albums/registration.html')


def register(request, username, email, password, r_password):
    try:
        User.objects.get(email=email)
        User.objects.get(username=username)
    except User.DoesNotExist:
        if password != r_password:
            raise AssertionError('Try again, password does not equal repeated password!')
        if User.objects.filter(username=username).exists():
            raise AssertionError('This user is already exists')
        try:
            validate_email(email)
        except ValidationError:
            raise AssertionError('Try again, bad email!')
        if len(username) < 8 or len(username) > 39:
            raise AssertionError('Try again, username length must be bigger than 7 symbols and less than 40 symbols!')
        if len(password) < 8 or len(password) > 39:
            raise AssertionError('Try again, password length must be bigger than 7 symbols and less than 40 symbols!')


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            error = 'Wrong username or password, try again, or try to'
            return render(request, 'albums/login.html', {
                'error': error,
            })
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('albums:index'))
    return render(request, 'albums/login.html')


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'albums/logout.html')
    else:
        return HttpResponseRedirect(reverse('albums:index'))


def profile(request, user_id):
    if request.user.is_authenticated:
        auth = True
        if request.user.id == user_id:
            request_user_profile = True
        else:
            request_user_profile = False
    else:
        auth = False
        request_user_profile = False
    user = get_object_or_404(User, pk=user_id)
    username = user.username
    rating_list = Rating.objects.filter(user=user)[:5]
    return render(request, 'albums/profile.html', {
        'username': username,
        'rating_list': rating_list,
        'auth': auth,
        'request_user_profile': request_user_profile,
        'user_id': user_id,
    })


def edit_profile(request):
    if request.user.is_authenticated:
        return render(request, 'albums/edit_profile.html')
    else:
        return HttpResponseRedirect(reverse('albums:index'))


def change_password(request):
    msg = ''
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            if user.check_password(old_password):
                if len(new_password) < 8 or len(new_password) > 39:
                    msg = 'Try again, new password length must be bigger than 7 symbols and less than 40 symbols!'
                else:
                    user.set_password(new_password)
                    user.save()
                    msg = 'Success!'
            else:
                msg = 'Wrong password, try again'
        return render(request, 'albums/change_password.html', {
            'msg': msg,
        })
    else:
        return HttpResponseRedirect(reverse('albums:index'))


def change_username(request):
    msg = ''
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            username = request.POST['username']
            if User.objects.filter(username=username).exists():
                msg = 'This username is already exists'
            else:
                if len(username) < 8 or len(username) > 39:
                    msg = 'Try again, username length must be bigger than 7 symbols and less than 40 symbols!'
                else:
                    user.username = username
                    user.save()
                    msg = 'Success!'
        return render(request, 'albums/change_username.html', {
            'msg': msg
        })
    else:
        return HttpResponseRedirect(reverse('albums:index'))


def search_rating(request, user_id, search_req):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    user_profile = get_object_or_404(User, pk=user_id)
    ratings = Rating.objects.filter(user=user_profile, album__name__icontains=search_req)
    return render(request, 'albums/search_rating.html', {
        'ratings': ratings,
        'search_req': search_req,
        'auth': auth,
        'username': username,
        'user': user,
        'user_id': user_id,
        'user_profile': user_profile,
    })


def more_alb_user(request, user_id, page_id):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    user_profile = get_object_or_404(User, pk=user_id)
    all_ratings = Rating.objects.filter(user=user_profile)
    page_all = ceil(len(all_ratings) / 4)
    page_ids = [i for i in range(1, page_all + 1)]
    ratings_on_page = list(all_ratings)[page_id * 4 - 4:page_id * 4]
    next_page = page_id + 1
    if page_id > 0:
        prev_page = page_id - 1
    else:
        prev_page = False
    if request.method == 'POST':
        search_req = request.POST['search']
        return search_rating(request, user_id, search_req)
    return render(request, 'albums/more_alb_user.html', {
        'ratings': ratings_on_page,
        'page_ids': page_ids,
        'next_page': next_page,
        'prev_page': prev_page,
        'auth': auth,
        'username': username,
        'user': user,
        'user_id': user_id,
        'user_profile': user_profile,
    })


def album_sort(request, by, rev, page_id):
    if request.user.is_authenticated:
        auth = True
        username = request.user.get_username()
        user = User.objects.get(pk=request.user.id)
    else:
        auth = False
        username = ''
        user = ''
    if rev == 'increasing':
        page_all = ceil(len(Album.objects.order_by(by)) / 4)
        page_ids = [i for i in range(1, page_all + 1)]
        albums_on_page = list(Album.objects.order_by(by))[page_id * 4 - 4:page_id * 4]
    if rev == 'descending':
        page_all = ceil(len(Album.objects.order_by('-' + by)) / 4)
        page_ids = [i for i in range(1, page_all + 1)]
        albums_on_page = list(Album.objects.order_by('-' + by))[page_id * 4 - 4:page_id * 4]
    next_page = page_id + 1
    if page_id > 0:
        prev_page = page_id - 1
    else:
        prev_page = False
    return render(request, 'albums/album_sort.html', {
        'albums': albums_on_page,
        'page_ids': page_ids,
        'next_page': next_page,
        'prev_page': prev_page,
        'auth': auth,
        'username': username,
        'user': user,
        'by1': by,
        'rev': rev,
    })
