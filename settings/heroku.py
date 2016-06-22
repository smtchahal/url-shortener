import dj_database_url

from .common import *

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIR = (
    os.path.join(BASE_DIR, 'static'),
)

DATABASES = {
    'default': dj_database_url.config(),
}

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']
