from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from interface.models import *
import socket

def index(request):

	render_vars = {
		'server_ip': '1.1.1.1',
		'server_name': socket.gethostname(),
	}

	return render_to_response('index.html', render_vars, context_instance=RequestContext(request))

def listen(request):

	if 'sort' in request.REQUEST and request.REQUEST['sort'] in ('sort_artist', 'sort_title', 'sort_album', '-sort_artist', '-sort_title', '-sort_album'):
		tracks = Track.objects.order_by(request.REQUEST['sort'])[:100]
		sort = request.REQUEST['sort']

	else:
		sort = None
		tracks = Track.objects.all()[:100]

	render_vars = {
		'tracks': tracks,
		'sort': sort,
		'artists': Track.objects.values('artist').distinct(),
	}

	return render_to_response('listen.html', render_vars, context_instance=RequestContext(request))