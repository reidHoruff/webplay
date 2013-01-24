from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import json
from django.forms import ModelForm
from interface.models import *
import os
import urllib

class ModelSerializer:

	def __init__(self, model=None):
		self.model = model

	class Meta:
		fields = None
		exclude = None

	def to_dict(self, string=True):
		if self.model is None:
			raise Exception('model is NoneType')

		field_names = set(map(lambda field: field.name, self.model._meta.fields))

		if hasattr(self.Meta, 'fields'):
			field_names = set(self.Meta.fields)

		if hasattr(self.Meta, 'exclude'):
			field_names -= set(self.Meta.exclude)

		out = {}

		for field_name in field_names:
			attr = getattr(self.model, field_name)

			if hasattr(attr, '__call__'):
				out[field_name] = attr()

			elif hasattr(attr, '__str__'):
				out[field_name] = str(attr)

		return out

class JSONResponse(HttpResponse):
	'''
	An HttpResponse that renders it's content into JSON.
	'''
	def __init__(self, data={}, success=True, message=None, **kwargs):
		return_obj = {}
		return_obj['message'] = message
		return_obj['success'] = success
		return_obj['data'] = data

		if settings.DEBUG:
			content = json.dumps(return_obj, indent=4, sort_keys=True)

		else:
			content = json.dumps(return_obj)

		kwargs['content_type'] = 'application/json'

		super(JSONResponse, self).__init__(content, **kwargs)

'''
decorators to make life so much easier
'''

def api_require_POST(function):
	def wrapper(request):
		if request.method == 'POST':
			return function(request)

		else:
			return JSONResponse(success=False, message='Request must be POST')

	return wrapper

def api_require_GET(function):
	def wrapper(request):
		if request.method == 'GET':
			return function(request)

		else:
			return JSONResponse(success=False, message='Request must be GET')

	return wrapper

def api_require_auth(function):
	def wrapper(request):

		if request.user.is_authenticated():
			return function(request)

		else:
			return JSONResponse(success=False, message='you must be authenticated')

	return wrapper

def get_curr_song():

	title = 'title'
	artist = 'artist'
	album = 'album'
	#title = os.popen('rhythmbox-client --print-playing-format=%tt').readline()
	#artist = os.popen('rhythmbox-client --print-playing-format=%ta').readline()
	#album = os.popen('rhythmbox-client --print-playing-format=%at').readline()

	output = os.popen('banshee --query-title --query-artist --query-album --query-volume')
	title = output.readline()[len('Title: '):]
	artist = output.readline()[len('Artist: '):]
	album = output.readline()[len('Album: '):]
	volume = output.readline()[len('volume: '):]
	
	data = {
		'title': title,
		'artist': artist,
		'album': album,
		'volume': volume,
	}

	return data

def play_track(request):

	if not 'track_id' in request.REQUEST:
		return JSONResponse(success=False, message='no track_id in request')


	track = Track.objects.get(id=request.REQUEST['track_id'])

	uri = urllib.quote(urllib.unquote(track.location))
	uri = track.location
	print uri

	os.popen('rhythmbox-client --play-uri=%s' % uri)
	return JSONResponse(data=get_curr_song(), message='track is playing')


def action_play(request):
	os.popen('banshee --play')
	#os.popen('rhythmbox-client --play')
	return JSONResponse(data=get_curr_song(), message='playing')

def action_pause(request):
	os.popen('banshee --pause')
	#os.popen('rhythmbox-client --pause')
	return JSONResponse(data=get_curr_song(), message='paused')

def action_next(request):
	os.popen('banshee --next')
	#os.popen('rhythmbox-client --next')
	return JSONResponse(data=get_curr_song(), message='next')

def action_previous(request):
	os.popen('banshee --previous')
	#os.popen('rhythmbox-client --previous')
	return JSONResponse(data=get_curr_song(), message='previous')

def action_get_info(request):
	return JSONResponse(data=get_curr_song(), message='here is your info!')

def action_mute(request):
	#os.popen('rhythmbox-client --mute')
	return JSONResponse(data=get_curr_song(), message='muted')

def action_unmute(request):
	#os.popen('rhythmbox-client --unmute')
	return JSONResponse(data=get_curr_song(), message='unmuted')

def action_volume_up(request):
	data = get_curr_song()

	data['volume'] = min(100, int(data['volume']) + 10)
	os.popen('banshee --set-volume=%s'%data['volume'])

	#os.popen('rhythmbox-client --volume-up')
	return JSONResponse(data=data, message='volume up')

def action_volume_down(request):
	data = get_curr_song()


	data['volume'] = max(0, int(data['volume']) - 10)
	os.popen('banshee --set-volume=%s'%data['volume'])

	#os.popen('rhythmbox-client --volume-down')
	return JSONResponse(data=data, message='volume down')