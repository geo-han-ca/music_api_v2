from django.db import models

class Song(models.Model):
    album = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    remote_url = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.playlist.name + ' - ' + self.song.title
