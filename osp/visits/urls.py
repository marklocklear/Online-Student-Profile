from django.conf.urls.defaults import *
from osp.visits import views

urlpatterns = patterns('',
    (r'^(?P<user_id>\d+)/log/', views.log, {}, 'log'),
    (r'^(?P<user_id>\d+)/all/(?P<page>\d+)/', views.view_all, {}, 'view-all'),
    (r'^(?P<user_id>\d+)/view/(?P<visit_id>\d+)/', views.view, {}, 'view'),
)
