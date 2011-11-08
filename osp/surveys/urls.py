from django.conf.urls.defaults import *

from osp.surveys import views

urlpatterns = patterns('',
    (r'^$', views.survey, {}, 'survey'),
    (r'^results/(?P<result_id>\d+)/$', views.results, {}, 'results'),
)
