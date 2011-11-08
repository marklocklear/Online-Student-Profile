from django.conf.urls.defaults import *

from osp.profiles import views

urlpatterns = patterns('',
    (r'^(?P<user_id>\d+)/', views.profile, {}, 'profile'),
)
