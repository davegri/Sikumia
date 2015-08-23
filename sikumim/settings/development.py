# -*- coding: utf-8 -*-
from .base import *



# memcache
CACHES = {
    'default' : {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
