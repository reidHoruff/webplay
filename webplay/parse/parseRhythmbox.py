from xml.dom import minidom
from os.path import expanduser
import os
import sys
from string import ascii_letters

def parse(file_path):

	Track.objects.all().delete()

	xmldoc = minidom.parse(file_path)

	for entry in xmldoc.getElementsByTagName('entry'):
		if entry.attributes['type'].value == 'song':

			artist = entry.getElementsByTagName('artist')[0].firstChild.nodeValue.encode('utf-8')
			title = entry.getElementsByTagName('title')[0].firstChild.nodeValue.encode('utf-8')
			album = entry.getElementsByTagName('album')[0].firstChild.nodeValue.encode('utf-8')

			entry = {
				'title': title,
				'artist': artist,
				'album': album,
				'sort_title': filter(lambda c: c in ascii_letters, title),
				'sort_artist': filter(lambda c: c in ascii_letters, artist),
				'sort_album': filter(lambda c: c in ascii_letters, album),
				'location': entry.getElementsByTagName('location')[0].firstChild.nodeValue.encode('utf-8'),
			}

			try:
				track = Track(**entry)
				track.save()
			except:
				print '%s by %s on %s' % (entry['title'], entry['artist'], entry['album'])

if __name__ == '__main__':
	sys.path.append('..')
	os.environ['DJANGO_SETTINGS_MODULE'] = 'webplay.settings'
	from django.core.management import setup_environ
	from webplay import settings
	setup_environ(settings)
	from interface.models import *
	parse(expanduser('~/.local/share/rhythmbox/rhythmdb.xml'))