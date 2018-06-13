from django.db import models

class Song(models.Model):
    rank = models.IntegerField(blank=True, null=True)
    song = models.CharField(max_length=200, blank=True, null=True)
    artist = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '%s - %s, by %s.' % (self.rank, self.song, self.artist)

    class Meta:
        ordering = ['rank',]
