from django.conf.urls.defaults import *

from osp.core import views

urlpatterns = patterns('',
    (r'^$', views.index, {}, 'index'),
    (r'^help/$', views.help, {}, 'help'),
    (r'^search/$', views.search, {}, 'search'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {}, 'logout'),
)
