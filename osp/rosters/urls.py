from django.conf.urls.defaults import *

from osp.rosters import views

urlpatterns = patterns('',
    (r'^(?P<section_id>\d+)/', views.roster, {}, 'roster'),
)
