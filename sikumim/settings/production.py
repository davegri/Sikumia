# -*- coding: utf-8 -*-
from .base import *
import dj_database_url

DEBUG = True

# HEROKU DEPLOYMENT

DATABASES['default'] = dj_database_url.config()


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# memcache
CACHES = 'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'TIMEOUT': 500,
            'BINARY': True,
            'OPTIONS': { 'tcp_nodelay': True }
}


