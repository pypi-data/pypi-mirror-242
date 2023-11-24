from .nbhandlers import commands
from .utils import init


init()

__version__ = "2.0.0a2"

__type__ = "plugin"
__name__ = "diviner"
__nbhandler__ = nbhandlers
__nbcommands__ = commands
__description__ = "基于古蓍草占卜算法."