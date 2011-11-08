from django.conf.urls.defaults import *

from osp.notifications import views

urlpatterns = patterns('',
    (r'^intervene/', views.notify, {
        'notification_type': 'intervention',
        'template': 'notifications/intervene.html'},
        'intervene'),
    (r'^contact/', views.notify, {}, 'contact'),
)
