from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'song', SongViewSet)
router.register(r'playlist', PlaylistViewSet)
router.register(r'playlistsong', PlaylistSongViewSet)

urlpatterns = [
 path('', include(router.urls)),
 path('ping/', ping, name='ping'),
 path('rawinfo/', rawinfo, name='rawinfo'),
 path('songs/', songs, name='songs'),
 path('albums/', albums, name='albums'),
 path('artists/', artists, name='artists'),
]