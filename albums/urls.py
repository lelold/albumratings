from django.urls import path

from . import views

app_name = 'albums'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:album_id>/', views.detail, name='detail'),
    path('page/<int:page_id>/', views.page, name='page'),
    path('artist/<int:artist_id>/', views.detail_artist, name='artist'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_username/', views.change_username, name='change_username'),
    path('search/<search_req>/', views.search, name='search'),
    path('user/<int:user_id>/more_alb_user/<int:page_id>/', views.more_alb_user, name='more_alb_user'),
    path('search_rating/<int:user_id>/', views.search_rating, name='search_rating'),
    path('album_sort/<by>/<rev>/<int:page_id>', views.album_sort, name='album_sort'),
    path('search_album/<search_req>/', views.search_album, name='search_album'),
    path('search_artist/<search_req>/', views.search_artist, name='search_artist'),
    path('search_user/<search_req>/', views.search_user, name='search_user'),
]
