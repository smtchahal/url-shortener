import os

from .common import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'test.sqlite3'),
    },
}

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.debug",
)
