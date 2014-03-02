from django.conf.urls import patterns, include, url


urlpatterns = patterns('app.views',
    url(r'^$', 'home'),

    url(r'^login/$', 'auth'),

    url(r'^signup/$', 'signup'),

    url(r'^logout/$', 'logout_view'),

    url(r'^myalerts/$', 'myalerts'),

    url(r'^newalert/$', 'new_alert'),

    url(r'^newlocation/$', 'new_location'),

    url(r'^deletealert/$', 'delete_alert'),

    url(r'^addalert/$', 'add_alert'),

    url(r'^banddetail/$', 'get_band_detail'),
)
