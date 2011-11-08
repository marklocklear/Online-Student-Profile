from django.conf.urls.defaults import *

from osp.api import views

urlpatterns = patterns('',
    (r'^instructor/import/', views.import_instructors, {},
        'import-instructors'),
    (r'^student/import/', views.import_students, {}, 'import-students'),
    (r'^section/import/', views.import_sections, {}, 'import-sections'),
    (r'^enrollment/import/', views.import_enrollments, {},
        'import-enrollments'),
)
