import os

from .common import *

try:
    from .dev import *
except ImportError:
    pass

try:
    from .prod import *
except ImportError:
    pass

if 'DYNO' in os.environ:
    from .heroku import *
