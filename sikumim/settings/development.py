# -*- coding: utf-8 -*-
from .base import *

# mailgun
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_HOST_USER = 'postmaster@sikumia.co.il'
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_PASSWORD']
EMAIL_PORT = 587

# memcache
CACHES = {
    'default' : {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
