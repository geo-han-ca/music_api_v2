from rest_framework import viewsets
from rest_framework.decorators import api_view #for views that dont have a model 
from rest_framework.response import Response
import requests
from django.utils.encoding import force_str #Python2 and 3 compatible way to convert to utf8 text

from rest_framework import filters

from .serializers import SongSerializer, PlaylistSerializer, PlaylistSongSerializer

from .models import Song, Playlist, PlaylistSong

from .music_processing import FileProcessing

@api_view(['GET'])
def rawinfo(request):
	response = requests.get("http://192.168.0.10:9010/showmusicfiles.php")
	mydata= response.json()
	return Response(mydata)

@api_view(['GET'])
def ping(request):
	return Response({"message": "musicapi is online and reachable"})

@api_view(['GET'])
def songs(request):
	if request.method == 'GET':
		if ('title' in request.GET) and ('artist' in request.GET):
			title = request.GET['title']
			artist = request.GET['artist']
			songInfo = FileProcessing.GetSingleSongJson(title, artist)
			return Response(songInfo)
		else:
			allSongs = FileProcessing.AllSongsJson()
			return Response(allSongs)

	return Response({"request not allowed: "+request.method+" musicapi/song"})

@api_view(['GET'])
def albums(request):
	if request.method == 'GET':
		if ('name' in request.GET) and ('artist' in request.GET):
			album = request.GET['name']
			artist = request.GET['artist']
			albumInfo = FileProcessing.GetSingleAlbumJson(album, artist)
			return Response(albumInfo)
		else:
			allAlbums = FileProcessing.AllAlbumsJson()
			return Response(allAlbums)

	return Response({"request not allowed: "+request.method+" musicapi/album"})

@api_view(['GET'])
def artists(request):
	if request.method == 'GET':
		if 'name' in request.GET:
			artist = request.GET['name']
			artistSongInfo = FileProcessing.GetSingleArtistSongsJson(artist)
			return Response(artistSongInfo)
		else:
			allArtists = FileProcessing.AllArtistsJson()
			return Response(allArtists)

	return Response({"request not allowed: "+request.method+" musicapi/artist"})

class SongViewSet(viewsets.ModelViewSet): 
	queryset = Song.objects.all()  
	serializer_class = SongSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'artist', 'album']  

class PlaylistViewSet(viewsets.ModelViewSet):  
	queryset = Playlist.objects.all()  
	serializer_class = PlaylistSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['name'] 

class PlaylistSongViewSet(viewsets.ModelViewSet):  
	queryset = PlaylistSong.objects.all()  
	serializer_class = PlaylistSongSerializer 
	filter_backends = [filters.SearchFilter]
	search_fields = ['playlist__id', 'song__id', 'playlist__name', 'song__title', 'song__artist', 'song__album', 'created_at'] 