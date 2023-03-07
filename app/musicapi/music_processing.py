import json
import urllib, requests, eyed3

class FileProcessing(object):

    def AllSongsJson():

        returnData = []

        raw_music_directory_contents = requests.get("http://192.168.0.10:9010/showmusicfiles.php")

        for file_path in raw_music_directory_contents.json():

            if ".mp3" not in file_path.lower():
                theMetadata = {'alert':'non-supported file'}
                returnData.append(theMetadata)
                continue
            
            song_url = "http://192.168.0.10:9010"+urllib.parse.quote(file_path[1:])

            song_meta_data = file_path[2:].split('/')

            theMetadata = {}

            theMetadata['artist'] = song_meta_data[0]
            theMetadata['album'] = song_meta_data[1]
            theMetadata['title'] = song_meta_data[2]
            theMetadata['remote_url'] = song_url

            returnData.append(theMetadata)
                    
        return returnData

    def AllAlbumsJson():

        returnData = []

        raw_music_directory_contents = requests.get("http://192.168.0.10:9010/showmusicfiles.php")

        for file_path in raw_music_directory_contents.json():

            if ".mp3" not in file_path.lower():
                # theMetadata = {'alert':'non-supported file'}
                # returnData.append(theMetadata)
                continue

            song_meta_data = file_path[2:].split('/')

            theMetadata = {}

            theMetadata['artist'] = song_meta_data[0]
            theMetadata['album'] = song_meta_data[1]

            if theMetadata not in returnData:
                returnData.append(theMetadata)
                    
        return returnData

    def AllArtistsJson():

        returnData = []

        raw_music_directory_contents = requests.get("http://192.168.0.10:9010/showmusicfiles.php")

        for file_path in raw_music_directory_contents.json():

            if ".mp3" not in file_path.lower():
                # theMetadata = {'alert':'non-supported file'}
                # returnData.append(theMetadata)
                continue

            song_meta_data = file_path[2:].split('/')

            theMetadata = {}

            theMetadata['artist'] = song_meta_data[0]

            if theMetadata not in returnData:
                returnData.append(theMetadata)
                    
        return returnData
    
    def GetSingleSongJson(title, artist):

        returnData = []

        raw_music_directory_contents = requests.get("http://192.168.0.10:9010/showmusicfiles.php")

        for file_path in raw_music_directory_contents.json():

            if ".mp3" not in file_path.lower():
                continue

            song_path = file_path[2:].split('/')
            # print( song_path[0] + ", " + song_path[2])
            
            if (artist in song_path[0]) and (title in song_path[2]):
                song_url = "http://192.168.0.10:9010"+urllib.parse.quote(file_path[1:])

                filename, headers = urllib.request.urlretrieve(song_url)
            
                audiofile = eyed3.load(filename)

                theMetadata = {}

                if audiofile.tag.artist:
                    theMetadata['artist'] = audiofile.tag.artist
                else:
                    theMetadata['artist'] = "unknown"

                if audiofile.tag.album:
                    theMetadata['album'] = audiofile.tag.album
                else:
                    theMetadata['album'] = "unknown"

                if audiofile.tag.title:
                    theMetadata['title'] = audiofile.tag.title
                else:
                    theMetadata['title'] = "unknown"

                theMetadata['remote_url'] = song_url

                returnData.append(theMetadata)

                break
                    
        return returnData

    def GetSingleArtistSongsJson(artist):

        returnData = []

        raw_music_directory_contents = requests.get("http://192.168.0.10:9010/showmusicfiles.php")

        for file_path in raw_music_directory_contents.json():

            if ".mp3" not in file_path.lower():
                continue

            song_path = file_path[2:].split('/')
            
            if artist in song_path[0]:
                song_url = "http://192.168.0.10:9010"+urllib.parse.quote(file_path[1:])

                filename, headers = urllib.request.urlretrieve(song_url)
            
                audiofile = eyed3.load(filename)

                theMetadata = {}

                if audiofile.tag.artist:
                    theMetadata['artist'] = audiofile.tag.artist
                else:
                    theMetadata['artist'] = "unknown"

                if audiofile.tag.album:
                    theMetadata['album'] = audiofile.tag.album
                else:
                    theMetadata['album'] = "unknown"

                if audiofile.tag.title:
                    theMetadata['title'] = audiofile.tag.title
                else:
                    theMetadata['title'] = "unknown"

                theMetadata['remote_url'] = song_url

                returnData.append(theMetadata)
                    
        return returnData

    def GetSingleAlbumJson(album, artist):

        returnData = []

        raw_music_directory_contents = requests.get("http://192.168.0.10:9010/showmusicfiles.php")

        for file_path in raw_music_directory_contents.json():

            if ".mp3" not in file_path.lower():
                continue

            song_path = file_path[2:].split('/')
            # print( song_path[0] + ", " + song_path[1])

            if (artist in song_path[0]) and (album in song_path[1]):
                song_url = "http://192.168.0.10:9010"+urllib.parse.quote(file_path[1:])

                filename, headers = urllib.request.urlretrieve(song_url)
            
                audiofile = eyed3.load(filename)

                theMetadata = {}

                if audiofile.tag.artist:
                    theMetadata['artist'] = audiofile.tag.artist
                else:
                    theMetadata['artist'] = "unknown"

                if audiofile.tag.album:
                    theMetadata['album'] = audiofile.tag.album
                else:
                    theMetadata['album'] = "unknown"

                if audiofile.tag.title:
                    theMetadata['title'] = audiofile.tag.title
                else:
                    theMetadata['title'] = "unknown"

                theMetadata['remote_url'] = song_url

                returnData.append(theMetadata)
                    
        return returnData
