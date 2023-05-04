from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_year = models.IntegerField()
    rating_all = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    rating_num = models.IntegerField(default=0)
    cover = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.name, self.artist)


class Rating(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_belong')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num = models.IntegerField(default=0)

    def __str__(self):
        return'Album: %s | User: %s | Rating: %s' % (self.album, self.user, self.num)