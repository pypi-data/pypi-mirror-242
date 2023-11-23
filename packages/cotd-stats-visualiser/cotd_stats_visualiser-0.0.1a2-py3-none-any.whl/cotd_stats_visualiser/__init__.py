import sys

if sys.version_info >= (3, 11):
    import asyncio
    import types

    asyncio.coroutine = types.coroutine  # type: ignore[attr-defined] # definitely not cursed

from .const import *  # noqa: F401, F403
from .main import *  # noqa: F401, F403
from .utils import *  # noqa: F401, F403
