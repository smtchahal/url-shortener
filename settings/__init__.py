import os

from .common import *  # noqa

try:
    from .dev import *  # noqa
except ImportError:
    pass

try:
    from .prod import *  # noqa
except ImportError:
    pass

if 'DYNO' in os.environ:
    from .heroku import *  # noqa
