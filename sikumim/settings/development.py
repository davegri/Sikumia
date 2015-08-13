# -*- coding: utf-8 -*-
from .base import *

DEBUG = True

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'testing@example.com'

# memcache
CACHES = 'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
}
