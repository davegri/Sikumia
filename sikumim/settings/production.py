# -*- coding: utf-8 -*-
from .base import *

DEBUG = False

#HEROKU DEPLOYMENT
import dj_database_url
DATABASES['default'] =  dj_database_url.config(default='postgres://david:david@localhost/sikumim_db')


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']
