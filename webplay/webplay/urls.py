from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

'''
admin
'''
urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
)

'''
interface app
'''
urlpatterns += patterns('interface.views',
	url(r'^$', 'index', name='index'),
	url(r'^listen/$', 'listen', name='listen'),
)

urlpatterns += patterns('interface.api',
	url(r'^wp_api/play_track$', 'play_track', name='play_track'),
	url(r'^wp_api/action_play$', 'action_play', name='action_play'),
	url(r'^wp_api/action_pause$', 'action_pause', name='action_pause'),
	url(r'^wp_api/action_previous$', 'action_previous', name='action_previous'),
	url(r'^wp_api/action_next$', 'action_next', name='action_next'),
	url(r'^wp_api/action_get_info$', 'action_get_info', name='action_get_info'),
	url(r'^wp_api/action_mute$', 'action_mute', name='action_mute'),
	url(r'^wp_api/action_unmute$', 'action_unmute', name='action_unmute'),
	url(r'^wp_api/action_volume_up$', 'action_volume_up', name='action_volume_up'),
	url(r'^wp_api/action_volume_down$', 'action_volume_down', name='action_volume_down'),
)

'''
static
'''
urlpatterns += patterns('',
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)