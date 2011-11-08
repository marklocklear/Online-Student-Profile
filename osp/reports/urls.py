from django.conf.urls.defaults import *

from osp.reports import views

urlpatterns = patterns('',
    (r'^learning/', views.learning_styles_report, {}, 'learning-styles-report'),
    (r'^personality/', views.personality_type_report, {}, 'personality-type-report'),
)
