"""

Yay! (nanameue, Inc.) API Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An API wrapper for Yay! (yay.space) written in Python.

:copyright: (c) 2023-present qvco
:license: MIT, see LICENSE for more details.

"""

from .client import *
from .config import *
from .errors import *
from .models import *
from .responses import *
from .utils import *
from .api.websocket import *

__version__ = Configs.YAYLIB_VERSION
__all__ = [
    "Client",
    "config",
    "errors",
    "models",
    "responses",
    "utils",
    "MessageEventHandler",
    "ChatRoomEventHandler",
    "GroupUpdateEventHandler",
    "GroupPostEventHandler",
]
