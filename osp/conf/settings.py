import os
import osp

SITE_ROOT = os.path.dirname(os.path.realpath(osp.__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'osp.core.middleware.http.Http403Middleware',
]

AUTH_PROFILE_MODULE = 'core.UserProfile'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

ROOT_URLCONF = 'osp.conf.urls'

TEMPLATE_DIRS = [
    os.path.join(SITE_ROOT, 'templates'),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'osp.core.context_processors.media_url',
    'osp.core.context_processors.base_template',
    'osp.core.context_processors.classes',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'south',
    'osp.api',
    'osp.assessments',
    'osp.core',
    'osp.notifications',
    'osp.profiles',
    'osp.reports',
    'osp.rosters',
    'osp.surveys',
    'osp.visits',
]
