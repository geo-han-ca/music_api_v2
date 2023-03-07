from django.test import LiveServerTestCase
from django.utils.encoding import force_str #Python2 and 3 compatible way to convert to utf8 text
import requests, json

## Music is stored in a directory in the format "./<Artist>/<Album>/<Song>"

class MusicApiTest(LiveServerTestCase):

    def __CountAlbums(self, allFiles):
        
        raw_music_directory_contents = allFiles

        albums = []
        for file_path in raw_music_directory_contents:

            if ".mp3" not in file_path.lower():
                continue

            #use artist/album combo because two or more artists can have albums with same name
            album = {file_path[2:].split('/')[0], file_path[2:].split('/')[1]}

            if album not in albums:
                albums.append(album)

                    
        return len(albums)

    def __CountArtists(self, allFiles):
        
        raw_music_directory_contents = allFiles

        artists = []
        for file_path in raw_music_directory_contents:

            if ".mp3" not in file_path.lower():
                continue

            artist = {file_path[2:].split('/')[0]}

            if artist not in artists:
                artists.append(artist)

                    
        return len(artists)

    def __CreatePlaylists(self, numberOfPlaylists):
        url = 'http://localhost:8000/musicapi/playlist/'

        allData = []
        for x in range(numberOfPlaylists):
            tmpName = {'name':'Test Playlist'+str(x + 1)}
            allData.append(tmpName)

        allresponses = []
        for single_name in allData:
            create_playlist_response = self.client.post(url, data=single_name)
            self.assertEqual(create_playlist_response.status_code, 201)
            allresponses.append(create_playlist_response)
    
        return allresponses

    def __AddSongsToDatabase(self, songs):
        url = 'http://localhost:8000/musicapi/song/'

        for song in songs:
            payload = {"album":song['album'], "artist":song['artist'], "title":song['title'], "remote_url":song['remote_url']}
            post_response = self.client.post(url, payload)
            self.assertEqual(post_response.status_code, 201)

    def __GetOneSongFromMusicServer(self, title, artist):
        single_song_response = requests.get("http://localhost:8000/musicapi/songs?title="+title+"&artist="+artist)
        self.assertEqual(single_song_response.status_code, 200)
        
        return single_song_response

    def __GetOneSongFromDatabase(self, title, artist):
        single_song_response = self.client.get("http://localhost:8000/musicapi/song/?search="+title+"+"+artist)
        self.assertEqual(single_song_response.status_code, 200)
        
        return single_song_response

    def __GetOnePlaylist(self, name):
        single_playlist_response = self.client.get("http://localhost:8000/musicapi/playlist/?search="+name)
        self.assertEqual(single_playlist_response.status_code, 200)
        
        return single_playlist_response

    # get ping (return api name)
    def test_can_ping(self):
        response = self.client.get("http://localhost:8000/musicapi/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_str(response.content), {'message':'musicapi is online and reachable'})

    # get music directory info
    def test_can_get_raw_info(self):
        raw_response = requests.get("http://192.168.0.10:9010/showmusicfiles.php")
        self.assertEqual(raw_response.status_code, 200)
        response = self.client.get("http://localhost:8000/musicapi/rawinfo/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_str(response.content), force_str(raw_response.content))

    # get all songs
    def test_can_get_all_songs(self):
        dir_contents_response = self.client.get("http://localhost:8000/musicapi/rawinfo/")
        self.assertEqual(dir_contents_response.status_code, 200)
        number_of_songs_on_server = len(dir_contents_response.json())
        all_songs_response = self.client.get("http://localhost:8000/musicapi/songs/")
        self.assertEqual(all_songs_response.status_code, 200)
        number_of_songs_processed = len(all_songs_response.json())
        self.assertEqual(number_of_songs_on_server, number_of_songs_processed)

    # get all albums
    def test_can_get_all_albums(self):
        dir_contents_response = self.client.get("http://localhost:8000/musicapi/rawinfo/")
        self.assertEqual(dir_contents_response.status_code, 200)
        number_of_albums_on_server = self.__CountAlbums(dir_contents_response.json())
        all_albums_response = self.client.get("http://localhost:8000/musicapi/albums/")
        self.assertEqual(all_albums_response.status_code, 200)
        number_of_albums_processed = len(all_albums_response.json())
        self.assertEqual(number_of_albums_on_server, number_of_albums_processed)

    # get all artists
    def test_can_get_all_artists(self):
        dir_contents_response = self.client.get("http://localhost:8000/musicapi/rawinfo/")
        self.assertEqual(dir_contents_response.status_code, 200)
        number_of_artists_on_server = self.__CountArtists(dir_contents_response.json())
        all_artists_response = self.client.get("http://localhost:8000/musicapi/artists/")
        self.assertEqual(all_artists_response.status_code, 200)
        number_of_artists_processed = len(all_artists_response.json())
        self.assertEqual(number_of_artists_on_server, number_of_artists_processed)

    # get single song
    def test_can_get_single_song(self):
        single_song_response = self.__GetOneSongFromMusicServer("Numb", "LINKIN PARK")
        number_of_songs_processed = len(single_song_response.json())
        self.assertEqual(number_of_songs_processed, 1)
        self.assertEqual('Numb', single_song_response.json()[0]['title'])
        self.assertEqual('LINKIN PARK', single_song_response.json()[0]['artist'])

    # get single artist (expect all songs from artist returned from api call)
    def test_can_get_single_artist(self):
        single_artist_response = self.client.get("http://localhost:8000/musicapi/artists/?name=LINKIN%20PARK")
        self.assertEqual(single_artist_response.status_code, 200)
        for songs in single_artist_response.json():
            self.assertEqual('LINKIN PARK', songs['artist'])

    # get single album (expect all songs for album returned by api call)
    def test_can_get_single_album(self):
        single_album_response = self.client.get("http://localhost:8000/musicapi/albums/?name=Greatest%20Hits&artist=LINKIN%20PARK")
        self.assertEqual(single_album_response.status_code, 200)
        for songs in single_album_response.json():
            self.assertEqual('Greatest Hits', songs['album'])
            self.assertEqual('LINKIN PARK', songs['artist'])
    
    # create new playlist
    def test_can_create_a_playlist(self):
        create_playlist_response = self.__CreatePlaylists(1)
        self.assertIn('Test Playlist1', create_playlist_response[0].content.decode())

    # get all playlists
    def test_can_get_all_playlists(self):
        self.__CreatePlaylists(2) 

        read_playlists_response = self.client.get('http://localhost:8000/musicapi/playlist/')
        self.assertEqual(read_playlists_response.status_code, 200)
        # print(read_playlists_response.json())
        html_response = read_playlists_response.content.decode()
        self.assertIn('Test Playlist1', html_response)
        self.assertIn('Test Playlist2', html_response)

    # get single playlist
    def test_can_get_single_playlist(self):
        self.__CreatePlaylists(2)

        single_playlist_response = self.__GetOnePlaylist("Test Playlist2")
        # print(single_playlist_response.json())
        number_of_playlists_processed = len(single_playlist_response.json())
        self.assertEqual(number_of_playlists_processed, 1)
        self.assertEqual('Test Playlist2', single_playlist_response.json()[0]['name'])

    # add song to playlist
    def test_can_add_song_to_playlist(self):
        self.__CreatePlaylists(1)
        self.__AddSongsToDatabase([
            {
                "artist": "LINKIN PARK",
                "album": "Greatest Hits",
                "title": "Numb.MP3",
                "remote_url": "http://192.168.0.10:9010/LINKIN%20PARK/Greatest%20Hits/Numb.MP3"
            }
        ])

        new_playlist = self.__GetOnePlaylist("Test Playlist1")
        
        existing_song = self.__GetOneSongFromDatabase("Numb", "LINKIN PARK")
       
        url = "http://localhost:8000/musicapi/playlistsong/"
        single_join = {"playlist_id":new_playlist.json()[0]['id'], "song_id":existing_song.json()[0]['id']}
        add_to_playlist_response = self.client.post(url, data=single_join)
        
        self.assertEqual(add_to_playlist_response.status_code, 201)
        self.assertEqual("Test Playlist1", add_to_playlist_response.json()['playlist']['name'])
        self.assertEqual("LINKIN PARK", add_to_playlist_response.json()['song']['artist'])
        self.assertEqual("Greatest Hits", add_to_playlist_response.json()['song']['album'])
        self.assertEqual("Numb.MP3", add_to_playlist_response.json()['song']['title'])
        self.assertEqual(
            "http://192.168.0.10:9010/LINKIN%20PARK/Greatest%20Hits/Numb.MP3", 
            add_to_playlist_response.json()['song']['remote_url']
            )

        # self.fail('add song to playlist todo')

    # delete song from playlist
    def test_can_delete_song_from_playlist(self):
        self.__CreatePlaylists(1)
        self.__AddSongsToDatabase([
            {
                "artist": "LINKIN PARK",
                "album": "Greatest Hits",
                "title": "Numb.MP3",
                "remote_url": "http://192.168.0.10:9010/LINKIN%20PARK/Greatest%20Hits/Numb.MP3"
            }
        ])

        existing_song = self.__GetOneSongFromDatabase("Numb", "LINKIN PARK")
        self.assertEqual(len(existing_song.json()), 1)

        url = 'http://localhost:8000/musicapi/song/'+str(existing_song.json()[0]['id'])+"/"
        delete_response = self.client.delete(url, existing_song.json()[0]['url'])
        self.assertEqual(delete_response.status_code, 204)

        existing_song = self.__GetOneSongFromDatabase("Numb", "LINKIN PARK")
        self.assertEqual(len(existing_song.json()), 0)
