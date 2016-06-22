import dj_database_url

from .common import *

DATABASES = {
    'default': dj_database_url.config(),
}

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']
