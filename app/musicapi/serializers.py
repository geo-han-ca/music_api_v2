from rest_framework import serializers 

from .models import Song, Playlist, PlaylistSong

class SongSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Song
        fields = ('url', 'id', 'title', 'remote_url', 'album', 'artist')

class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Playlist
        fields = ('url', 'id', 'name')

class PlaylistSongSerializer(serializers.HyperlinkedModelSerializer):
    playlist = PlaylistSerializer(read_only=True)
    song = SongSerializer(read_only=True)
    playlist_id = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all(), source='playlist', write_only=True)
    song_id = serializers.PrimaryKeyRelatedField(queryset=Song.objects.all(), source='song', write_only=True)

    class Meta:
        model = PlaylistSong
        fields = ('url', 'id', 'playlist_id', 'playlist', 'song_id', 'song', 'created_at')