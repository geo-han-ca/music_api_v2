from django.test import TestCase
from musicapi.models import Song, Playlist, PlaylistSong

class SongModelTest(TestCase):

    def test_saving_and_reading_songs(self):
        songObject = Song()
        songObject.artist = 'Foo'
        songObject.album = 'Foo_Album'
        songObject.title = 'Foo Title'
        songObject.remote_url = 'http://foo-host/foo/path'
        songObject.save()

        saved_songs = Song.objects.all()
        self.assertEqual(saved_songs.count(), 1)

        first_saved_song = saved_songs[0]
        self.assertEqual(first_saved_song.artist, 'Foo')
        self.assertEqual(first_saved_song.album, 'Foo_Album')
        self.assertEqual(first_saved_song.title, 'Foo Title')
        self.assertEqual(first_saved_song.remote_url, 'http://foo-host/foo/path')

class PlaylistModelTest(TestCase):

    def test_saving_and_reading_playlist_names(self):
        playlistObject = Playlist()
        playlistObject.name = 'Test Playlist'
        playlistObject.save()

        saved_playlists = Playlist.objects.all()
        self.assertEqual(saved_playlists.count(), 1)

        first_saved_playlist = saved_playlists[0]
        self.assertEqual(first_saved_playlist.name, 'Test Playlist')
        
class PlaylistSongModelTest(TestCase):

    def test_saving_and_reading_playlistsong_joins(self):
        songObject = Song()
        songObject.artist = 'Foo3'
        songObject.album = 'Foo_Album3'
        songObject.title = 'Foo Title3'
        songObject.remote_url = 'http://foo-host/foo/path3'
        songObject.save()

        playlistObject = Playlist()
        playlistObject.name = 'Test Playlist3'
        playlistObject.save()

        saved_songs = Song.objects.all()
        saved_playlists = Playlist.objects.all()

        playlistSongObject = PlaylistSong()
        playlistSongObject.song = saved_songs[0]
        playlistSongObject.playlist = saved_playlists[0]
        playlistSongObject.save()

        saved_playlistsongs = PlaylistSong.objects.all()
        self.assertEqual(saved_playlistsongs.count(), 1)

        first_saved_playlistsong = saved_playlistsongs[0]
        self.assertEqual(first_saved_playlistsong.playlist.name, 'Test Playlist3')
        self.assertEqual(first_saved_playlistsong.song.artist, 'Foo3')
        self.assertEqual(first_saved_playlistsong.song.album, 'Foo_Album3')
        self.assertEqual(first_saved_playlistsong.song.title, 'Foo Title3')
        self.assertEqual(first_saved_playlistsong.song.remote_url, 'http://foo-host/foo/path3')
