from osp.conf.settings import *

# Unique key used for salting passwords
SECRET_KEY = 'Chac-8#haCa_Ra-e?-e+ucrur=gEFRasejayasaC?meMe!AC-a'

# DEBUG should be False in production, True in development
DEBUG = False

# List of administrators who should receive error reports
ADMINS = (
    ('John Smith', 'john.smith@example.edu'),
    ('Francis Drake', 'francis.drake@example.edu'),
)
MANAGERS = ADMINS

# List of developers who receive email messages in debug mode
DEBUG_USERS = ADMINS

# MySQL database configuration settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'osp',
        'USER': 'osp',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Server time zone
TIME_ZONE = 'America/New_York'

# Used if you are hosting OSP off the top level (e.g. http://example.edu/osp/)
URL_PREFIX = ''

# The URL path at which media is being served
MEDIA_URL = URL_PREFIX + '/media/'

# The URL path at which admin media is being served
ADMIN_MEDIA_PREFIX = URL_PREFIX + '/media/admin/'


# Uncomment the following lines if you are using the LDAP backend
#
# import ldap
# from django_auth_ldap.config import LDAPSearch
#
# AUTHENTICATION_BACKENDS = [
#     'django_auth_ldap.backend.LDAPBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]
# AUTH_LDAP_SERVER_URI = 'ldap://ldap.example.edu'
# AUTH_LDAP_BIND_DN = 'service_user'
# AUTH_LDAP_BIND_PASSWORD = 'service_password'
# AUTH_LDAP_USER_SEARCH = LDAPSearch('ou=Users,dc=example,dc=edu',
#                                    ldap.SCOPE_SUBTREE,
#                                    '(uid=%(user)s)')
# AUTH_LDAP_USER_ATTR_MAP = {
#     'first_name': 'givenName',
#     'last_name': 'sn',
#     'email': 'mail'
# }
# LOGIN_REDIRECT_URL = URL_PREFIX + '/'


# Uncomment the following lines if you are using the CAS backend
#
# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'django_cas.backends.CASBackend',
# ]
# MIDDLEWARE_CLASSES.append('django_cas.middleware.CASMiddleware')
# CAS_VERSION = '1'
# CAS_SERVER_URL = 'https://cas.example.edu'
# CAS_IGNORE_REFERER = True
# CAS_REDIRECT_URL = URL_PREFIX + '/'


# The URL paths for login and logout pages
LOGIN_URL = URL_PREFIX + '/login/'
LOGOUT_URL = URL_PREFIX + '/logout/'

# SMTP mail server configuration settings
EMAIL_HOST = 'smtp.example.edu'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'service_user'
EMAIL_HOST_PASSWORD = 'service_password'

# List of IP addresses for hosts allowed to push data to the API
API_ALLOWED_HOSTS = []

# Authorization key for pushing data to the API
API_KEY = ''

# Email address that intervention requests are sent to
INTERVENTIONS_EMAIL = 'interventions@example.edu'

# "From" email address for the application
SERVER_EMAIL = 'osp@example.edu'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# All potential term choices that could be received by the API
TERM_CHOICES = [
    ('fa', 'Fall'),
    ('sp', 'Spring'),
    ('su', 'Summer'),
]

# Current year and term
CURRENT_TERM = 'su'
CURRENT_YEAR = 2011

# All potential enrollment status choices that could be received by the API
ENROLLMENT_STATUS_CHOICES = [
    ('A', 'Active'),
    ('D', 'Dropped'),
    ('W', 'Withdrawn'),
    ('X', 'Deleted'),
    ('C', 'Cancelled'),
    ('NP', 'Non-payment'),
]

# Enrollment statuses which are considered "active"
ACTIVE_ENROLLMENT_STATUSES = ['A',]

# List of campuses for your school
CAMPUS_CHOICES = [
    'Main',
    'Uptown',
]

# List of contact types for visits
VISIT_CONTACT_TYPE_CHOICES = [
    'In Person',
    'Email',
    'Telephone',
    'Online',
    'Group Session',
]

# List of reasons for visits
VISIT_REASON_CHOICES = [
    'New Student Admission',
    'Academic Advising',
    'Counseling',
    'Personal Counseling',
    'Early Alert Referral',
    'Graduation Assessment Review',
    'Career Counseling',
    'Workshops, Class Presentations',
    'Early Alert Counseling',
    'Disability Counseling',
    'Faculty Advising',
    'Academic Warning',
    'Academic Probation',
    'First Academic Suspension',
    'Final Academic Suspension',
]

# List of departments for visits
VISIT_DEPARTMENT_CHOICES = [
    'Advising',
    'Counseling',
]

# List of Career Services outcomes for visits
VISIT_CAREER_SERVICES_OUTCOME_CHOICES = [
    'No Contact',
    'Email',
    'Phone',
    'Scheduled Appointment with Career Services',
    'No Show for Appointment',
    'Took Career Assessment(s)',
    'Met with Career Counselor',
    'Career Decision in Process',
    'Career and Program Decision Completed',
    'Referred for Program Update',
    'Program Updated',
]

# List of intervention reasons
INTERVENTION_REASONS = [
    'Excessive Tardiness/Absenteeism',
    'Failing Test/Quiz Scores',
    'Missing Assignments',
    'Needs Personal or Social Counseling',
    'Needs Career Exploration',
    'Needs Tutoring',
]

# Re-structure the choices lists for Django's sake
CAMPUS_CHOICES = [(x, x) for x in CAMPUS_CHOICES]
VISIT_CONTACT_TYPE_CHOICES = [(x, x) for x in VISIT_CONTACT_TYPE_CHOICES]
VISIT_REASON_CHOICES = [(x, x) for x in VISIT_REASON_CHOICES]
VISIT_DEPARTMENT_CHOICES = [(x, x) for x in VISIT_DEPARTMENT_CHOICES]
VISIT_CAREER_SERVICES_OUTCOME_CHOICES = [(x, x) for x in
                                         VISIT_CAREER_SERVICES_OUTCOME_CHOICES]
INTERVENTION_REASONS = [(x, x) for x in INTERVENTION_REASONS]
