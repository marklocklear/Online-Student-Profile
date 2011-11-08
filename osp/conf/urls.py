from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('osp.api.urls', namespace='api', app_name='api')),
    (r'^assessment/',
     include('osp.assessments.urls',
             namespace='assessment',
             app_name='assessment')),
    (r'^notification/',
     include('osp.notifications.urls',
             namespace='notification',
             app_name='notification')),
    (r'^profile/',
     include('osp.profiles.urls', namespace='profile', app_name='profile')),
    (r'^roster/',
     include('osp.rosters.urls', namespace='roster', app_name='roster')),
    (r'^survey/',
     include('osp.surveys.urls', namespace='survey', app_name='survey')),
    (r'^visit/',
     include('osp.visits.urls', namespace='visit', app_name='visit')),
    (r'^report/',
     include('osp.reports.urls', namespace='report', app_name='report')),
    (r'^', include('osp.core.urls', namespace='core', app_name='core')),
    (r'^accounts/password/change/$', 'password_change', {}, 'password_change_form'),
    (r'^accounts/password/change/$', 'password_change_done', {}, 'password_change_done'),
)

if 'django_cas.middleware.CASMiddleware' in settings.MIDDLEWARE_CLASSES:
    urlpatterns += patterns('django_cas.views',
        (r'^login/$', 'login', {}, 'login'),
        (r'^logout/$', 'logout', {}, 'logout'),
    )
else:
    urlpatterns += patterns('django.contrib.auth.views',
        (r'^login/$', 'login', {}, 'login'),
        (r'^logout/$', 'logout', {}, 'logout'),
    )

if settings.DEBUG:
    MEDIA_URL = settings.MEDIA_URL
    if MEDIA_URL.startswith('/'):
        MEDIA_URL = MEDIA_URL[1:]

    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % MEDIA_URL,
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
