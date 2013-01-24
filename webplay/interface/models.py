from django.db import models

class Track(models.Model):
	artist = models.CharField(max_length=500)
	title = models.CharField(max_length=500)
	album = models.CharField(max_length=500)
	location = models.CharField(max_length=1000)

	sort_artist = models.CharField(max_length=500)
	sort_title = models.CharField(max_length=500)
	sort_album = models.CharField(max_length=500)

	def __unicode__(self):
		return "%s by %s on %s" % (self.title, self.artist, self.album)