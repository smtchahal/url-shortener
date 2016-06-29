import dj_database_url

from .common import *  # noqa

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500),
}

DEBUG = False

ALLOWED_HOSTS = ['*']
